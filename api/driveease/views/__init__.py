"""Domain-organized API views."""

from .accounts import (
    AccountsListView,
    AccountsStatsView,
    AssignAccountRoleView,
    AdminEditAccountView,
)

from .dashboard import (
    AdminDashboardRevenueView,
)

from .fleet import (
    CarListView,
    FleetListView,
    CarDetailView,
    FleetStatsView,
    CarCreateView,
    CarTypeListView,
    FeatureListCreateView,
    CarUpdateView,
    CarDeleteView,
)

from .reviews import (
    ReviewListView,
    CarReviewListView,
    FeaturedReviewsView,
    CreateReviewView,
    UpdateReviewView,
    DeleteReviewView,
    AdminReviewListView,
    AdminReviewStatusView,
    AdminDeleteReviewView,
    toggle_helpful,
)

from .contacts import (
    ContactListView,
    ContactCreateView,
    ContactDetailView,
    SubmitToGmail,
)

from .uploads import (
    FileUploadView,
)

from .bookings import (
    CreateBookingView,
    TransactionListView,
    TransactionDetailView,
    AdminBookingListView,
    AdminBookingStatsView,
    AdminCreateBookingView,
    AdminUpdateBookingView,
    AdminBookingDeleteView,
)

from .payments import (
    CreatePayMongoPaymentView,
    PayMongoWebhookView,
)

from .notifications import (
    UserNotificationListView,
    UserUnreadNotificationCountView,
    MarkNotificationAsReadView,
)

__all__ = [
    'AccountsListView',
    'AccountsStatsView',
    'AssignAccountRoleView',
    'AdminEditAccountView',
    'AdminDashboardRevenueView',
    'CarListView',
    'FleetListView',
    'CarDetailView',
    'FleetStatsView',
    'CarCreateView',
    'CarTypeListView',
    'FeatureListCreateView',
    'CarUpdateView',
    'CarDeleteView',
    'ReviewListView',
    'CarReviewListView',
    'FeaturedReviewsView',
    'CreateReviewView',
    'UpdateReviewView',
    'DeleteReviewView',
    'AdminReviewListView',
    'AdminReviewStatusView',
    'AdminDeleteReviewView',
    'toggle_helpful',
    'ContactListView',
    'ContactCreateView',
    'ContactDetailView',
    'SubmitToGmail',
    'FileUploadView',
    'CreateBookingView',
    'TransactionListView',
    'TransactionDetailView',
    'AdminBookingListView',
    'AdminBookingStatsView',
    'AdminCreateBookingView',
    'AdminUpdateBookingView',
    'AdminBookingDeleteView',
    'CreatePayMongoPaymentView',
    'PayMongoWebhookView',
    'UserNotificationListView',
    'UserUnreadNotificationCountView',
    'MarkNotificationAsReadView',
]
