import os
import requests
from django.conf import settings
from django.core import signing
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
import urllib.parse

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .utils.auth import is_authorized
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from .models import FileUploadModel

User = get_user_model()

def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        value=str(refresh_token),
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        httponly=True,
        secure=settings.JWT_REFRESH_COOKIE_SECURE,
        samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
        domain=settings.JWT_REFRESH_COOKIE_DOMAIN,
        path=settings.JWT_REFRESH_COOKIE_PATH,
    )
    return response

def delete_refresh_cookie(response):
    response.delete_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        domain=settings.JWT_REFRESH_COOKIE_DOMAIN,
        path=settings.JWT_REFRESH_COOKIE_PATH,
        samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
    )
    return response

def get_frontend_url():
    return os.getenv(
        "FRONTEND_DRIVEEASE_URL",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ).rstrip('/')

def get_allowed_frontend_urls():
    configured_urls = os.getenv("FRONTEND_ALLOWED_ORIGINS", "")
    allowed_urls = {
        url.strip().rstrip('/')
        for url in configured_urls.split(',')
        if url.strip()
    }
    allowed_urls.add(get_frontend_url())
    return allowed_urls

def get_safe_frontend_url(candidate):
    normalized = (candidate or "").rstrip('/')
    return normalized if normalized in get_allowed_frontend_urls() else get_frontend_url()

def has_allowed_browser_origin(request):
    origin = request.headers.get("Origin")
    return not origin or origin.rstrip('/') in get_allowed_frontend_urls()

def get_backend_url(request):
    host = request.get_host()
    if host.startswith('127.0.0.1'):
        host = host.replace('127.0.0.1', 'localhost')
    return f"{request.scheme}://{host}"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = f"{get_backend_url(request)}/api/driveease/auth/google/callback/"
        
        origin = get_safe_frontend_url(request.GET.get('origin'))
        state_data = {
            'redirect_uri': redirect_uri,
            'frontend_url': origin,
        }
        state = signing.dumps(state_data, salt='driveease-google-oauth')
        
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        })
        return redirect(url)

class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        error = request.GET.get('error')
        code = request.GET.get('code')

        frontend_url = get_frontend_url()

        # User cancelled login
        if error == 'access_denied':
            return redirect(f"{frontend_url}/client/login?error=cancelled")

        # Missing code
        if not code:
            return redirect(f"{frontend_url}/client/login?error=no_code")

        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        redirect_uri = f"{get_backend_url(request)}/auth/google/callback/"

        state_param = request.GET.get('state')

        if state_param:
            try:
                state_data = signing.loads(
                    state_param,
                    salt='driveease-google-oauth',
                    max_age=600,
                )

                redirect_uri = state_data.get('redirect_uri', redirect_uri)
                frontend_url = get_safe_frontend_url(
                    state_data.get('frontend_url')
                )

            except signing.BadSignature:
                return redirect(f"{frontend_url}/client/login?error=oauth_failed")
        else:
            return redirect(f"{frontend_url}/client/login?error=oauth_failed")

        try:

            token_res = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code',
                }
            ).json()

            if 'access_token' not in token_res:
                print("[ERROR] No access token received")
                return redirect(f"{frontend_url}/client/login?error=oauth_failed")

            profile_res = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={
                    'Authorization': f"Bearer {token_res['access_token']}"
                }
            ).json()

            if not is_authorized(profile_res):
                return redirect(f"{frontend_url}/client/login?error=unauthorized")

            auth_user, created = User.objects.get_or_create(
                username=profile_res["email"],
                defaults={
                    "email": profile_res["email"],
                    "first_name": profile_res.get("given_name", ""),
                    "last_name": profile_res.get("family_name", ""),
                    "profile_picture": profile_res.get("picture", ""),
                }
            )

            refresh = RefreshToken.for_user(auth_user)

            if auth_user.is_staff:
                response = redirect(f"{frontend_url}/admin/admin-dashboard/")
                return set_refresh_cookie(response, refresh)

            response = redirect(f"{frontend_url}/")
            return set_refresh_cookie(response, refresh)

        except Exception:
            return redirect(f"{frontend_url}/client/login?error=oauth_failed")

class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "given_name": user.first_name,
            "family_name": user.last_name,
            "email": user.email,

            "contact_number": user.contact_number,
            "address": user.address,
            "profile_picture": user.profile_picture,
            "id_images": user.id_images,

            "date_created": user.date_joined.isoformat(),
        })
    
    def patch(self, request):
        user = request.user
        data = request.data

        # Update user fields
        user.first_name = data.get("given_name", user.first_name)
        user.last_name = data.get("family_name", user.last_name)
        user.email = data.get("email", user.email)

        user.contact_number = data.get(
            "contact_number",
            user.contact_number
        )

        user.address = data.get(
            "address",
            user.address
        )
        
        old_profile_picture = user.profile_picture

        new_profile_picture = data.get(
            "profile_picture",
            old_profile_picture,
        )

        user.profile_picture = new_profile_picture

        user.id_images = data.get(
            "id_images",
            user.id_images,
        )

        deleted_images = list(data.get("deleted_images", []))

        if (
            old_profile_picture
            and new_profile_picture != old_profile_picture
        ):
            deleted_images.append(old_profile_picture)

        user.save()

        for upload in FileUploadModel.objects.exclude(file=""):
            if upload.file.url in deleted_images:
                upload.file.delete(save=False)
                upload.delete()

        return Response({
            "message": "Profile updated successfully"
        })

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if not has_allowed_browser_origin(request):
            return Response({"detail": "Invalid origin"}, status=403)

        refresh_token = request.COOKIES.get(settings.JWT_REFRESH_COOKIE_NAME)

        if not refresh_token:
            return Response({"detail": "No refresh token"}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        response = Response({
            "access": serializer.validated_data["access"],
        })
        rotated_refresh = serializer.validated_data.get("refresh")

        if rotated_refresh:
            set_refresh_cookie(response, rotated_refresh)

        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not has_allowed_browser_origin(request):
            return Response({"detail": "Invalid origin"}, status=403)

        refresh_token = request.COOKIES.get(settings.JWT_REFRESH_COOKIE_NAME)

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                # Logout is intentionally idempotent. An expired, malformed,
                # or already-blacklisted token is already unusable.
                pass

        response = Response(status=status.HTTP_204_NO_CONTENT)
        return delete_refresh_cookie(response)
