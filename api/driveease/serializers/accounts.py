from rest_framework import serializers

from ..models import Accounts
from ..utils.roles import ACCOUNT_ROLES, ROLE_FLAGS, get_account_role


class AccountsSerializer(serializers.ModelSerializer):
    given_name = serializers.CharField(source='first_name')
    family_name = serializers.CharField(source='last_name')
    status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    rentals = serializers.IntegerField(read_only=True)

    class Meta:
        model = Accounts
        fields = [
            'id', 'user_reference', 'email', 'given_name', 'family_name',
            'contact_number', 'address', 'profile_picture', 'id_images',
            'date_joined', 'status', 'role', 'rentals',
        ]

    def get_status(self, obj):
        return 'Active' if obj.is_active else 'Suspended'

    def get_role(self, obj):
        return get_account_role(obj)


class AdminCreateAccountSerializer(serializers.ModelSerializer):
    given_name = serializers.CharField(source="first_name", max_length=150)
    family_name = serializers.CharField(source="last_name", max_length=150)
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=ACCOUNT_ROLES,
        write_only=True,
    )
    id_images = serializers.JSONField(required=True)

    class Meta:
        model = Accounts
        fields = [
            "given_name",
            "family_name",
            "email",
            "contact_number",
            "address",
            "id_images",
            "role",
        ]
        extra_kwargs = {
            "contact_number": {"required": False, "allow_blank": True},
            "address": {"required": False, "allow_blank": True},
        }

    def validate_email(self, value):
        normalized_email = value.strip().lower()
        if Accounts.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError(
                "An account with this email address already exists."
            )
        return normalized_email

    def validate_id_images(self, value):
        images = value.get("images") if isinstance(value, dict) else None
        if not isinstance(images, list):
            raise serializers.ValidationError(
                "ID documents must be provided as a list."
            )
        if len(images) > 5:
            raise serializers.ValidationError(
                "A maximum of five ID documents is allowed."
            )

        url_field = serializers.URLField()
        try:
            validated_images = [url_field.run_validation(url) for url in images]
        except serializers.ValidationError:
            raise serializers.ValidationError(
                "Every ID document must contain a valid uploaded file URL."
            )
        return {"images": validated_images}

    def create(self, validated_data):
        role = validated_data.pop("role")
        email = validated_data.pop("email")
        account = Accounts(
            username=email,
            email=email,
            **ROLE_FLAGS[role],
            **validated_data,
        )
        # Authentication is Google-only; this account must never accept a
        # local password. Google OAuth will reuse it through its email/username.
        account.set_unusable_password()
        account.save()
        return account


class AdminEditAccountSerializer(serializers.ModelSerializer):
    given_name = serializers.CharField(
        source="first_name", required=False, allow_blank=True, max_length=150
    )
    family_name = serializers.CharField(
        source="last_name", required=False, allow_blank=True, max_length=150
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    contact_number = serializers.CharField(required=False, allow_blank=True, max_length=20)
    address = serializers.CharField(required=False, allow_blank=True)
    remove_profile_picture = serializers.BooleanField(
        required=False, default=False, write_only=True
    )
    profile_removal_reason = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    remove_id_images = serializers.ListField(
        child=serializers.CharField(), required=False, default=list, write_only=True
    )
    id_removal_reason = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )
    id_images = serializers.JSONField(required=False, write_only=True)
    role = serializers.ChoiceField(
        choices=ACCOUNT_ROLES,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Accounts
        fields = [
            "given_name", "family_name", "email", "contact_number", "address",
            "remove_profile_picture", "profile_removal_reason", "remove_id_images",
            "id_removal_reason", "id_images",
            "role",
        ]

    def validate_email(self, value):
        existing = Accounts.objects.filter(email__iexact=value)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate(self, attrs):
        remove_profile = attrs.get("remove_profile_picture", False)
        profile_reason = attrs.get("profile_removal_reason", "").strip()
        selected_ids = attrs.get("remove_id_images", [])
        id_reason = attrs.get("id_removal_reason", "").strip()
        new_id_images = attrs.get("id_images")

        if remove_profile:
            if not self.instance.profile_picture:
                raise serializers.ValidationError({
                    "remove_profile_picture": "This account has no profile picture to remove."
                })
            if not profile_reason:
                raise serializers.ValidationError({
                    "profile_removal_reason": "A reason is required to remove the profile picture."
                })

        if selected_ids:
            current_images = (self.instance.id_images or {}).get("images", [])
            if not isinstance(current_images, list):
                raise serializers.ValidationError({
                    "remove_id_images": "The account's ID image data is invalid."
                })
            if len(selected_ids) != len(set(selected_ids)):
                raise serializers.ValidationError({
                    "remove_id_images": "Duplicate ID image selections are not allowed."
                })
            if any(image not in current_images for image in selected_ids):
                raise serializers.ValidationError({
                    "remove_id_images": "One or more selected ID images no longer exist. Refresh and try again."
                })
            if not id_reason:
                raise serializers.ValidationError({
                    "id_removal_reason": "A reason is required to remove ID images."
                })

        if new_id_images is not None:
            new_images = new_id_images.get("images") if isinstance(new_id_images, dict) else None
            if not isinstance(new_images, list):
                raise serializers.ValidationError({
                    "id_images": "ID documents must be provided as a list."
                })
            if len(new_images) != len(set(new_images)):
                raise serializers.ValidationError({
                    "id_images": "Duplicate ID documents are not allowed."
                })

            url_field = serializers.URLField()
            try:
                validated_new_images = [url_field.run_validation(url) for url in new_images]
            except serializers.ValidationError:
                raise serializers.ValidationError({
                    "id_images": "Every ID document must contain a valid uploaded file URL."
                })

            current_images = (self.instance.id_images or {}).get("images", [])
            retained_images = [
                image for image in current_images if image not in selected_ids
            ]
            if len(retained_images) + len(validated_new_images) > 5:
                raise serializers.ValidationError({
                    "id_images": "A maximum of five ID documents is allowed."
                })
            attrs["id_images"] = {"images": validated_new_images}
        return attrs

    def update(self, instance, validated_data):
        role = validated_data.pop("role", None)
        remove_profile = validated_data.pop("remove_profile_picture", False)
        validated_data.pop("profile_removal_reason", None)
        selected_ids = validated_data.pop("remove_id_images", [])
        validated_data.pop("id_removal_reason", None)
        new_id_images = validated_data.pop("id_images", None)

        if remove_profile:
            instance.profile_picture = None
        if selected_ids:
            id_images = instance.id_images or {}
            instance.id_images = {
                **id_images,
                "images": [
                    image for image in id_images.get("images", []) if image not in selected_ids
                ],
            }
        if new_id_images:
            id_images = instance.id_images or {}
            instance.id_images = {
                **id_images,
                "images": [
                    *id_images.get("images", []),
                    *new_id_images["images"],
                ],
            }
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if role:
            for field, value in ROLE_FLAGS[role].items():
                setattr(instance, field, value)
        instance.save()
        return instance


class RoleAssignmentSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=ACCOUNT_ROLES)


class AccountStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
