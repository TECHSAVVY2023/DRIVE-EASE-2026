
from django.urls import path
from . import views_auth
from . import views

urlpatterns = [
    # Auth endpoints
    path('auth/google/', views_auth.GoogleLoginView.as_view(), name='auth-google'),
    path('auth/google/callback/', views_auth.GoogleCallbackView.as_view(), name='auth-google-callback'),
    path('auth/me/', views_auth.AuthMeView.as_view(), name='auth-me'),

    path('auth/token/refresh/', views_auth.CookieTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/', views_auth.LogoutView.as_view(), name='auth-logout'),

    path("uploads/", views.FileUploadView.as_view(), name="file-upload"),

    path('users/', views.AccountsListView.as_view(), name='accounts-list'),
    path('users/stats/', views.AccountsStatsView.as_view(), name='accounts-stats'),
    path('admin/accounts/', views.AdminCreateAccountView.as_view(), name='admin-create-account'),
    path('users/<str:user_reference>/role/', views.AssignAccountRoleView.as_view(), name='account-assign-role'),

    path("admin/accounts/<str:user_reference>/", views.AdminEditAccountView.as_view(), name="admin-edit-account"),
    path("admin/accounts/<str:user_reference>/status/", views.AccountStatusUpdateView.as_view(), name="account-update-status"),

    path("admin/dashboard/revenue/", views.AdminDashboardRevenueView.as_view(), name="admin-dashboard-revenue"),
    path("admin/dashboard/stats/", views.AdminDashboardStatsView.as_view(), name="admin-dashboard-stats"),
    path("admin/dashboard/fleet-status/", views.AdminDashboardFleetStatusView.as_view(), name="admin-dashboard-fleet-status"),
    path("admin/dashboard/recent-bookings/", views.AdminDashboardRecentBookingsView.as_view(), name="admin-dashboard-recent-bookings"),
    path("admin/dashboard/attention/", views.AdminDashboardAttentionView.as_view(), name="admin-dashboard-attention"),
    path("admin/analytics/stats/", views.AdminAnalyticsStatsView.as_view(), name="admin-analytics-stats"),
    path("admin/analytics/revenue/", views.AdminAnalyticsRevenueView.as_view(), name="admin-analytics-revenue"),
    path("admin/analytics/status-distribution/", views.AdminAnalyticsStatusDistributionView.as_view(), name="admin-analytics-status-distribution"),
    path("admin/analytics/top-vehicles/", views.AdminAnalyticsTopVehiclesView.as_view(), name="admin-analytics-top-vehicles"),
    path("admin/analytics/customer-insights/", views.AdminAnalyticsCustomerInsightsView.as_view(), name="admin-analytics-customer-insights"),

    path('contact/list/', views.ContactListView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view()),
    path('contact/delete/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/edit/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/create/', views.ContactCreateView.as_view()),
    path('contact/gmail-notif/', views.SubmitToGmail.as_view()),

    path("fleet/", views.FleetListView.as_view(), name="fleet-list"),
    path("fleet/stats/", views.FleetStatsView.as_view()),

    path("cars/", views.CarListView.as_view(), name="car-list"),
    path("cars/create/", views.CarCreateView.as_view(), name="car-create"),
    path("cars/update/<str:car_reference>/", views.CarUpdateView.as_view(), name="car-update"),
    path("cars/delete/<str:car_reference>/", views.CarDeleteView.as_view(), name="car-delete"),
    path("cars/<str:car_reference>/", views.CarDetailView.as_view()),
    path("cars/<str:car_reference>/similar/", views.SimilarCarListView.as_view(), name="similar-cars"),
    
    path("car-types/", views.CarTypeListView.as_view(), name="car-types"),
    path( "features/", views.FeatureListCreateView.as_view(), name="feature-list-create", ),
    
    path("reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("reviews/cars/<str:car_reference>/create/", views.CreateReviewView.as_view(), name="create-review"),
    path("reviews/cars/<str:car_reference>/delete/<str:review_reference>/", views.DeleteReviewView.as_view(), name="delete-review"),
    path("reviews/cars/<str:car_reference>/edit/<str:review_reference>/", views.UpdateReviewView.as_view(), name="update-review"),
    path("cars/<str:car_reference>/reviews/", views.CarReviewListView.as_view()),
    path("reviews/featured/", views.FeaturedReviewsView.as_view(), name="featured-reviews"),
    path("reviews/<str:review_reference>/helpful/", views.toggle_helpful, name="toggle-helpful"),

    path("admin/reviews/", views.AdminReviewListView.as_view(), name="admin-reviews"),
    path("admin/reviews/<str:review_reference>/status/", views.AdminReviewStatusView.as_view(), name="admin-review-status"),
    path("admin/reviews/<str:review_reference>/delete/", views.AdminDeleteReviewView.as_view(), name="admin-delete-review"),

    path("bookings/create/", views.CreateBookingView.as_view(), name="create-booking"),
    path("bookings/", views.TransactionListView.as_view(), name="bookings"),
    path("bookings/<str:booking_reference>/", views.TransactionDetailView.as_view(), name="booking-detail"),
    path("bookings/<str:booking_reference>/cancel/", views.ClientCancelBookingView.as_view(), name="booking-cancel"),
    
    path("admin/bookings/create/", views.AdminCreateBookingView.as_view(), name="admin-booking-create"),
    path("admin/bookings/", views.AdminBookingListView.as_view(), name="admin-bookings"),
    path("admin/bookings/stats/", views.AdminBookingStatsView.as_view(), name="admin-booking-stats"),
    path("admin/bookings/update/<str:booking_reference>/", views.AdminUpdateBookingView.as_view(), name="admin-booking-update"),
    path("admin/bookings/delete/<str:booking_reference>/", views.AdminBookingDeleteView.as_view(), name="admin-booking-delete"),

    path("admin/logs/", views.AdminActivityLogListView.as_view(), name="admin-activity-logs"),

    path("payments/create-paymongo-payment/", views.CreatePayMongoPaymentView.as_view(), name="create-paymongo-payment"),
    path("admin/bookings/<str:booking_reference>/refund/", views.AdminIssueRefundView.as_view(), name="admin-booking-refund"),
    path("payments/paymongo-webhook/", views.PayMongoWebhookView.as_view(), name="paymongo-webhook"),  # Commented out for development

    path("notifications/", views.UserNotificationListView.as_view(), name="user-notifications"),
    path("notifications/unread-count/", views.UserUnreadNotificationCountView.as_view(), name="notification-unread-count"),
    path("notifications/read-all/", views.UserMarkAllNotificationsAsReadView.as_view(), name="notifications-read-all"),
    path("notifications/delete-all/", views.UserDeleteAllNotificationsView.as_view(), name="notifications-delete-all"),
    path("notifications/<int:notification_id>/read/", views.MarkNotificationAsReadView.as_view(), name="mark-notification-read"),
    path("cars/<str:car_reference>/availability-alert/", views.CarAvailabilityAlertView.as_view(), name="car-availability-alert"),

    path("admin/notifications/", views.AdminNotificationListView.as_view(), name="admin-notifications"),
    path("admin/notifications/unread-count/", views.AdminUnreadNotificationCountView.as_view(), name="admin-notification-unread-count"),
    path("admin/notifications/read-all/", views.AdminMarkAllNotificationsAsReadView.as_view(), name="admin-notifications-read-all"),
    path("admin/notifications/<int:notification_id>/read/", views.AdminMarkNotificationAsReadView.as_view(), name="admin-notification-read"),
    path("admin/notifications/<int:notification_id>/", views.AdminDeleteNotificationView.as_view(), name="admin-notification-delete"),

    path("content/home/", views.PublicHomePageContentView.as_view(), name="public-homepage-content"),
    path("admin/content/home/edit/", views.HomePageContentUpdateView.as_view(), name="admin-content-edit"),
    path("admin/content/home/trust-items/", views.TrustItemListCreateView.as_view(), name="admin-content-trust-items"),
    path("admin/content/home/trust-items/<int:pk>/", views.TrustItemDetailView.as_view(), name="admin-content-trust-item-detail"),
    path("admin/content/home/featured-cars/", views.FeaturedCarListCreateView.as_view(), name="admin-content-featured-cars"),
    path("admin/content/home/featured-cars/<int:pk>/", views.FeaturedCarDetailView.as_view(), name="admin-content-featured-car-detail"),

    path("content/about/", views.PublicAboutUsContentView.as_view(), name="public-about-content"),
    path("admin/content/about/edit/", views.AboutUsContentUpdateView.as_view(), name="admin-about-content-edit"),
    path("admin/content/about/team-users/", views.AboutTeamUserOptionsView.as_view(), name="admin-about-team-users"),
    path("content/contact/", views.PublicContactPageContentView.as_view(), name="public-contact-content"),
    path("admin/content/contact/edit/", views.ContactPageContentUpdateView.as_view(), name="admin-contact-content-edit"),
]
