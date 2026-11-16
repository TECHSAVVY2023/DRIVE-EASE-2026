from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from ..models import AdminActivityLog
from ..pagination import AdminActivityLogPagination
from ..serializers import AdminActivityLogSerializer

class AdminActivityLogListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminActivityLogSerializer
    pagination_class = AdminActivityLogPagination

    def get_queryset(self):
        queryset = AdminActivityLog.objects.select_related("admin").all()

        # Search
        search = self.request.query_params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(admin__email__icontains=search) |
                Q(admin__username__icontains=search) |
                Q(admin__first_name__icontains=search) |
                Q(admin__last_name__icontains=search) |
                Q(target_type__icontains=search) |
                Q(target_id__icontains=search)
            )

        # Action filter
        action = self.request.query_params.get("action")

        if action and action != "all":
            queryset = queryset.filter(action=action)

        # Target type filter
        target_type = self.request.query_params.get("target_type")

        if target_type and target_type != "all":
            queryset = queryset.filter(target_type__iexact=target_type)

        # Sorting
        sort = self.request.query_params.get("sort")

        if sort == "oldest":
            queryset = queryset.order_by("created_at", "id")
        else:
            queryset = queryset.order_by("-created_at", "-id")

        return queryset
