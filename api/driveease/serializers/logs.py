from rest_framework import serializers

from ..models import AdminActivityLog


class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin_name = serializers.SerializerMethodField()
    admin_reference = serializers.CharField(
        source="admin.user_reference", read_only=True, allow_null=True
    )
    admin_profile_picture = serializers.URLField(
        source="admin.profile_picture", read_only=True, allow_null=True
    )

    class Meta:
        model = AdminActivityLog
        fields = [
            "id", "admin", "admin_name", "admin_profile_picture", "admin_reference",
            "action", "description", "target_type", "target_id", "created_at",
        ]
        read_only_fields = fields

    def get_admin_name(self, obj):
        if obj.admin:
            return obj.admin.get_full_name() or obj.admin.email or obj.admin.username
        return "Deleted Admin"
