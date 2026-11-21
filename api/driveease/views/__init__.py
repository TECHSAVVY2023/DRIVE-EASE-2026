"""Domain-organized API views."""

from .accounts import (
    AccountsListView,
    AccountsStatsView,
    AdminCreateAccountView,
    AssignAccountRoleView,
    AdminEditAccountView,
    AccountStatusUpdateView,
)

from .dashboard import (
    AdminDashboardRevenueView,
    AdminDashboardStatsView,
    AdminDashboardFleetStatusView,
    AdminDashboardRecentBookingsView,
    AdminDashboardAttentionView,
)

from .fleet import (
    CarListView,
    FleetListView,
    CarDetailView,
    SimilarCarListView,
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
    ClientCancelBookingView,
    AdminBookingListView,
    AdminBookingStatsView,
    AdminCreateBookingView,
    AdminUpdateBookingView,
    AdminBookingDeleteView,
)

from .payments import (
    AdminIssueRefundView,
    CancelPayMongoPaymentView,
    CreatePayMongoPaymentView,
    PayMongoWebhookView,
)

from .notifications import (
    UserNotificationListView,
    UserUnreadNotificationCountView,
    MarkNotificationAsReadView,
    UserMarkAllNotificationsAsReadView,
    UserDeleteAllNotificationsView,
    CarAvailabilityAlertView,
    AdminNotificationListView,
    AdminUnreadNotificationCountView,
    AdminMarkNotificationAsReadView,
    AdminMarkAllNotificationsAsReadView,
    AdminDeleteNotificationView,
)

from .analytics import (
    AdminAnalyticsStatsView,
    AdminAnalyticsRevenueView,
    AdminAnalyticsStatusDistributionView,
    AdminAnalyticsTopVehiclesView,
    AdminAnalyticsCustomerInsightsView,
)

from .logs import (
    AdminActivityLogListView,
)

from .content import (
    PublicHomePageContentView,
    HomePageContentUpdateView,
    FeaturedCarListCreateView,
    FeaturedCarDetailView,
    TrustItemListCreateView,
    TrustItemDetailView,
    FAQListCreateView,
    FAQDetailView,
    PublicAboutUsContentView,
    AboutUsContentUpdateView,
    AboutTeamUserOptionsView,
    PublicContactPageContentView,
    ContactPageContentUpdateView,
)

__all__ = [
    'AccountsListView',
    'AccountsStatsView',
    'AdminCreateAccountView',
    'AssignAccountRoleView',
    'AdminEditAccountView',
    'AdminDashboardRevenueView',
    'CarListView',
    'FleetListView',
    'CarDetailView',
    'SimilarCarListView',
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
    'ClientCancelBookingView',
    'AdminBookingListView',
    'AdminBookingStatsView',
    'AdminCreateBookingView',
    'AdminUpdateBookingView',
    'AdminBookingDeleteView',
    'CancelPayMongoPaymentView',
    'CreatePayMongoPaymentView',
    'AdminIssueRefundView',
    'PayMongoWebhookView',
    'UserNotificationListView',
    'UserUnreadNotificationCountView',
    'MarkNotificationAsReadView',
    'UserMarkAllNotificationsAsReadView',
    'UserDeleteAllNotificationsView',
    'CarAvailabilityAlertView',
    'AdminNotificationListView',
    'AdminUnreadNotificationCountView',
    'AdminMarkNotificationAsReadView',
    'AdminMarkAllNotificationsAsReadView',
    'AdminDeleteNotificationView',
    'AccountStatusUpdateView',
    'AdminActivityLogListView',
    'AdminDashboardStatsView',
    'AdminDashboardFleetStatusView',
    'AdminDashboardRecentBookingsView',
    'AdminDashboardAttentionView',
    'AdminAnalyticsStatsView',
    'AdminAnalyticsRevenueView',
    'AdminAnalyticsStatusDistributionView',
    'AdminAnalyticsTopVehiclesView',
    'AdminAnalyticsCustomerInsightsView',
    'PublicHomePageContentView',
    'HomePageContentUpdateView',
    'FeaturedCarListCreateView',
    'FeaturedCarDetailView',
    'TrustItemListCreateView',
    'TrustItemDetailView',
    'FAQListCreateView',
    'FAQDetailView',
    'PublicAboutUsContentView',
    'AboutUsContentUpdateView',
    'AboutTeamUserOptionsView',
    'PublicContactPageContentView',
    'ContactPageContentUpdateView',
]
