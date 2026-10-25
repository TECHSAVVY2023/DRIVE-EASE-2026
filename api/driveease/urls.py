
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
    path('users/<int:user_id>/role/', views.AssignAccountRoleView.as_view(), name='account-assign-role'),

    path("admin/accounts/<int:user_id>/", views.AdminEditAccountView.as_view(), name="admin-edit-account"),
    path("admin/accounts/<int:user_id>/status/", views.AccountStatusUpdateView.as_view(), name="account-update-status"),

    path("admin/dashboard/revenue/", views.AdminDashboardRevenueView.as_view(), name="admin-dashboard-revenue"),

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
    path("cars/update/<str:car_id>/", views.CarUpdateView.as_view(), name="car-update"),
    path("cars/delete/<str:car_id>/", views.CarDeleteView.as_view(), name="car-delete"),
    path("cars/<str:car_id>/", views.CarDetailView.as_view()),
    
    path("car-types/", views.CarTypeListView.as_view(), name="car-types"),
    path( "features/", views.FeatureListCreateView.as_view(), name="feature-list-create", ),
    
    path("reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("reviews/cars/<str:car_id>/create/", views.CreateReviewView.as_view(), name="create-review"),
    path("reviews/cars/<str:car_id>/delete/<str:review_id>/", views.DeleteReviewView.as_view(), name="delete-review"),
    path("reviews/cars/<str:car_id>/edit/<str:review_id>/", views.UpdateReviewView.as_view(), name="update-review"),
    path("cars/<str:car_id>/reviews/", views.CarReviewListView.as_view()),
    path("reviews/featured/", views.FeaturedReviewsView.as_view(), name="featured-reviews"),
    path("reviews/<int:review_id>/helpful/", views.toggle_helpful, name="toggle-helpful"),

    path("admin/reviews/", views.AdminReviewListView.as_view(), name="admin-reviews"),
    path("admin/reviews/<int:review_id>/status/", views.AdminReviewStatusView.as_view(), name="admin-review-status"),
    path("admin/reviews/<int:review_id>/delete/", views.AdminDeleteReviewView.as_view(), name="admin-delete-review"),

    path("bookings/create/", views.CreateBookingView.as_view(), name="create-booking"),
    path("bookings/", views.TransactionListView.as_view(), name="bookings"),
    path("bookings/<str:booking_reference>/", views.TransactionDetailView.as_view(), name="booking-detail"),
    
    path("admin/bookings/create/", views.AdminCreateBookingView.as_view(), name="admin-booking-create"),
    path("admin/bookings/", views.AdminBookingListView.as_view(), name="admin-bookings"),
    path("admin/bookings/stats/", views.AdminBookingStatsView.as_view(), name="admin-booking-stats"),
    path("admin/bookings/update/<str:booking_reference>/", views.AdminUpdateBookingView.as_view(), name="admin-booking-update"),
    path("admin/bookings/delete/<str:booking_reference>/", views.AdminBookingDeleteView.as_view(), name="admin-booking-delete"),

    path("payments/create-paymongo-payment/", views.CreatePayMongoPaymentView.as_view(), name="create-paymongo-payment"),
    path("payments/paymongo-webhook/", views.PayMongoWebhookView.as_view(), name="paymongo-webhook"),  # Commented out for development

    path("notifications/", views.UserNotificationListView.as_view(), name="user-notifications"),
    path("notifications/unread-count/", views.UserUnreadNotificationCountView.as_view(), name="notification-unread-count"),
    path("notifications/<int:notification_id>/read/", views.MarkNotificationAsReadView.as_view(), name="mark-notification-read"),
]
