"""Accounts API views."""

import logging

from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Accounts, AdminActivityLog, FileUploadModel
from ..pagination import AccountsPagination
from ..tasks import create_notification
from ..serializers import (
    AccountsSerializer,
    RoleAssignmentSerializer,
    AdminEditAccountSerializer,
    AccountStatusSerializer,
)

logger = logging.getLogger(__name__)


def delete_account_uploads_from_storage(urls):
    """Delete app-managed uploads matching the supplied account URLs."""
    urls_to_delete = {url for url in urls if url}

    if not urls_to_delete:
        return

    for upload in FileUploadModel.objects.exclude(file=""):
        try:
            upload_url = upload.file.url
        except Exception:
            logger.exception(
                "Could not resolve uploaded file URL for upload %s.",
                upload.pk,
            )
            continue

        if upload_url not in urls_to_delete:
            continue

        # FieldFile.delete removes the object through the configured
        # S3-compatible storage backend. The model row is removed next.
        upload.file.delete(save=False)
        upload.delete()

class AccountsListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AccountsSerializer
    pagination_class = AccountsPagination

    def get_queryset(self):
        queryset = (
            Accounts.objects
            .annotate(rentals=Count('bookings'))
            .order_by('-date_joined')
        )

        # Search
        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        # Status
        status = self.request.query_params.get('status')

        if status == 'Active':
            queryset = queryset.filter(is_active=True)

        elif status == 'Suspended':
            queryset = queryset.filter(is_active=False)

        # Role
        role = self.request.query_params.get('role')

        if role == 'Super Admin':
            queryset = queryset.filter(is_superuser=True)

        elif role == 'Admin':
            queryset = queryset.filter(
                is_staff=True,
                is_superuser=False
            )

        elif role == 'User':
            queryset = queryset.filter(
                is_staff=False,
                is_superuser=False
            )

        return queryset

class AccountsStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = Accounts.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(is_active=True)),
            suspended=Count('id', filter=Q(is_active=False)),
        )

        return Response(stats)


class AssignAccountRoleView(APIView):
    permission_classes = [IsAdminUser]

    ROLE_FLAGS = {
        "User": {
            "is_staff": False,
            "is_superuser": False,
        },
        "Admin": {
            "is_staff": True,
            "is_superuser": False,
        },
        "Super Admin": {
            "is_staff": True,
            "is_superuser": True,
        },
    }

    @transaction.atomic
    def patch(self, request, user_id):
        serializer = RoleAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = get_object_or_404(Accounts, pk=user_id)
        new_role = serializer.validated_data["role"]
        old_role = AccountsSerializer().get_role(account)

        if account.pk == request.user.pk:
            return Response(
                {"detail": "You cannot change your own role."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            new_role == "Super Admin"
            and not request.user.is_superuser
        ):
            return Response(
                {
                    "detail": (
                        "Only a Super Admin can assign the "
                        "Super Admin role."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if account.is_superuser and not request.user.is_superuser:
            return Response(
                {
                    "detail": (
                        "Only a Super Admin can change another "
                        "Super Admin's role."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if (
            account.is_superuser
            and new_role != "Super Admin"
            and Accounts.objects.filter(is_superuser=True).count() <= 1
        ):
            return Response(
                {"detail": "The last Super Admin cannot be demoted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_role == new_role:
            return Response(
                {"detail": f"This user is already a {new_role}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        flags = self.ROLE_FLAGS[new_role]
        account.is_staff = flags["is_staff"]
        account.is_superuser = flags["is_superuser"]
        account.save(update_fields=["is_staff", "is_superuser"])

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description=(
                f"Changed {account.email or account.username}'s role "
                f"from {old_role} to {new_role}."
            ),
            target_type="user",
            target_id=str(account.pk),
        )

        account = (
            Accounts.objects
            .annotate(rentals=Count("bookings"))
            .get(pk=account.pk)
        )

        return Response(
            {
                "message": "User role updated successfully.",
                "user": AccountsSerializer(account).data,
            },
            status=status.HTTP_200_OK,
        )

class AdminEditAccountView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, user_id):
        account = get_object_or_404(
            Accounts.objects.select_for_update(),
            pk=user_id,
        )

        # A regular admin cannot edit a Super Admin's account.
        if (
            account.is_superuser
            and not request.user.is_superuser
        ):
            return Response(
                {
                    "detail": (
                        "Only a Super Admin can edit "
                        "another Super Admin's account."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AdminEditAccountSerializer(
            account,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        # Capture removal details before the serializer consumes them.
        data = serializer.validated_data
        remove_profile = data.get(
            "remove_profile_picture", False
        )
        profile_reason = data.get(
            "profile_removal_reason", ""
        ).strip()

        selected_ids = data.get("remove_id_images", [])
        id_reason = data.get(
            "id_removal_reason", ""
        ).strip()
        profile_picture_url = (
            account.profile_picture if remove_profile else None
        )

        # Save account changes and requested removals.
        serializer.save()

        # Remove only files managed through FileUploadModel. This leaves
        # external profile URLs (for example, Google avatars) untouched.
        delete_account_uploads_from_storage([
            profile_picture_url,
            *selected_ids,
        ])

        account_label = account.email or account.username

        # Record ordinary account edits.
        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description=(
                f"Updated account details for {account_label}."
            ),
            target_type="user",
            target_id=str(account.pk),
        )

        # Record the profile picture removal and queue its notification.
        if remove_profile:
            AdminActivityLog.objects.create(
                admin=request.user,
                action="update",
                description=(
                    f"Removed profile picture for {account_label}. "
                    f"Reason: {profile_reason}"
                ),
                target_type="user",
                target_id=str(account.pk),
            )

            transaction.on_commit(
                lambda uid=account.pk, reason=profile_reason:
                    create_notification.delay(
                        uid,
                        "system",
                        "Profile Picture Removed",
                        (
                            "An administrator removed your profile "
                            f"picture. Reason: {reason}"
                        ),
                        action_url="/client/profile",
                    )
            )

        # Record the ID image removal and queue its notification.
        if selected_ids:
            removed_count = len(selected_ids)

            AdminActivityLog.objects.create(
                admin=request.user,
                action="update",
                description=(
                    f"Removed {removed_count} ID image(s) for "
                    f"{account_label}. Reason: {id_reason}"
                ),
                target_type="user",
                target_id=str(account.pk),
            )

            transaction.on_commit(
                lambda uid=account.pk, reason=id_reason,
                       count=removed_count:
                    create_notification.delay(
                        uid,
                        "system",
                        "ID Documents Removed",
                        (
                            f"An administrator removed {count} of "
                            "your ID document(s). "
                            f"Reason: {reason} "
                            "Please visit your account page to "
                            "upload replacement documents if needed."
                        ),
                        action_url="/client/profile",
                    )
            )

        # Return the same user representation as the accounts list.
        updated_account = (
            Accounts.objects
            .annotate(rentals=Count("bookings"))
            .get(pk=account.pk)
        )

        return Response(
            {
                "message": "Account updated successfully.",
                "user": AccountsSerializer(
                    updated_account
                ).data,
            },
            status=status.HTTP_200_OK,
        )

class AccountStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, user_id):
        serializer = AccountStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = get_object_or_404(
            Accounts.objects.select_for_update(),
            pk=user_id,
        )

        new_is_active = serializer.validated_data["is_active"]
        old_status = "Active" if account.is_active else "Suspended"
        new_status = "Active" if new_is_active else "Suspended"

        # Prevent admins from changing their own account status.
        if account.pk == request.user.pk:
            return Response(
                {"detail": "You cannot change your own account status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Only Super Admins can change another Super Admin's status.
        if account.is_superuser and not request.user.is_superuser:
            return Response(
                {
                    "detail": (
                        "Only a Super Admin can change another "
                        "Super Admin's account status."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Prevent suspending the last active Super Admin.
        if (
            account.is_superuser
            and account.is_active
            and not new_is_active
            and Accounts.objects.filter(
                is_superuser=True,
                is_active=True,
            ).count() <= 1
        ):
            return Response(
                {
                    "detail": (
                        "The last active Super Admin cannot be suspended."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Avoid logging an action when the status hasn't changed.
        if account.is_active == new_is_active:
            return Response(
                {
                    "message": f"Account is already {new_status}.",
                    "user": AccountsSerializer(account).data,
                },
                status=status.HTTP_200_OK,
            )

        account.is_active = new_is_active
        account.save(update_fields=["is_active"])

        AdminActivityLog.objects.create(
            admin=request.user,
            action="status_change",
            description=(
                f"Changed {account.email or account.username}'s "
                f"account status from {old_status} to {new_status}."
            ),
            target_type="user",
            target_id=str(account.pk),
        )

        account = (
            Accounts.objects
            .annotate(rentals=Count("bookings"))
            .get(pk=account.pk)
        )

        return Response(
            {
                "message": f"Account {new_status.lower()} successfully.",
                "user": AccountsSerializer(account).data,
            },
            status=status.HTTP_200_OK,
        )

