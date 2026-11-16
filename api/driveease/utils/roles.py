USER_ROLE = "Customer"
ADMIN_ROLE = "Admin"
SUPER_ADMIN_ROLE = "Super Admin"
ACCOUNT_ROLES = (USER_ROLE, ADMIN_ROLE, SUPER_ADMIN_ROLE)

ROLE_FLAGS = {
    USER_ROLE: {"is_staff": False, "is_superuser": False},
    ADMIN_ROLE: {"is_staff": True, "is_superuser": False},
    SUPER_ADMIN_ROLE: {"is_staff": True, "is_superuser": True},
}


def get_account_role(account):
    if account.is_superuser:
        return SUPER_ADMIN_ROLE
    if account.is_staff:
        return ADMIN_ROLE
    return USER_ROLE


def can_manage_account(actor, target):
    """Admins manage users; Super Admins manage every account tier."""
    return actor.is_superuser or not target.is_staff


def can_assign_role(actor, role):
    """Only Super Admins can create or assign staff-level roles."""
    return actor.is_superuser or role == USER_ROLE
