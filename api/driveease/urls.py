
from django.urls import path
from . import views_auth
from . import views
from .views import CarListView, CarDetailView, FileUploadView

urlpatterns = [
    # Auth endpoints
    path('auth/google/', views_auth.GoogleLoginView.as_view(), name='auth-google'),
    path('auth/google/callback/', views_auth.GoogleCallbackView.as_view(), name='auth-google-callback'),
    path('auth/me/', views_auth.AuthMeView.as_view(), name='auth-me'),
    path('auth/logout/', views_auth.AuthLogoutView.as_view(), name='auth-logout'),

    path('auth/token/refresh/', views_auth.CookieTokenRefreshView.as_view()),

    path("uploads/", views.FileUploadView.as_view(), name="file-upload"),

    path('contact/list/', views.ContactListView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view()),
    path('contact/delete/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/edit/<int:pk>/', views.ContactCreateView.as_view()),
    path('contact/create/', views.ContactCreateView.as_view()),
    path('contact/gmail-notif/', views.SubmitToGmail.as_view()),

    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<str:car_id>/", views.CarDetailView.as_view())
]