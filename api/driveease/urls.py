
from django.urls import path
from . import views_auth
from . import views

urlpatterns = [
    # Auth endpoints
    path('auth/google/', views_auth.GoogleLoginView.as_view(), name='auth-google'),
    path('auth/google/callback/', views_auth.GoogleCallbackView.as_view(), name='auth-google-callback'),
    path('auth/me/', views_auth.AuthMeView.as_view(), name='auth-me'),

    path('auth/token/refresh/', views_auth.CookieTokenRefreshView.as_view()),

    path("uploads/", views.FileUploadView.as_view(), name="file-upload"),

    path('contact/list/', views.ContactListView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view()),
    path('contact/delete/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/edit/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/create/', views.ContactCreateView.as_view()),
    path('contact/gmail-notif/', views.SubmitToGmail.as_view()),

    path("cars/", views.CarListView.as_view(), name="car-list"),
    path("cars/<str:car_id>/", views.CarDetailView.as_view()),
    
    path("reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("reviews/cars/<str:car_id>/create/", views.CreateReviewView.as_view(), name="create-review"),
    path("reviews/cars/<str:car_id>/delete/<str:review_id>/", views.DeleteReviewView.as_view(), name="delete-review"),
    path("reviews/cars/<str:car_id>/edit/<str:review_id>/", views.UpdateReviewView.as_view(), name="update-review"),
    path("cars/<str:car_id>/reviews/", views.CarReviewListView.as_view()),
    path("reviews/featured/", views.FeaturedReviewsView.as_view(), name="featured-reviews"),
    path("reviews/<int:review_id>/helpful/", views.toggle_helpful, name="toggle-helpful"),

    path("bookings/create/", views.CreateBookingView.as_view(), name="create-booking"),
    path("payments/create-paymongo-payment/", views.CreatePayMongoPaymentView.as_view(), name="create-paymongo-payment"),
    path("payments/paymongo-webhook/", views.PayMongoWebhookView.as_view(), name="paymongo-webhook"),  # Commented out for development
]