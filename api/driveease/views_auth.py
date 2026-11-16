import os
import logging
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
from .utils.roles import get_account_role

User = get_user_model()
logger = logging.getLogger(__name__)

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
    configured_url = os.getenv("BACKEND_URL", "").strip().rstrip("/")
    if configured_url:
        return configured_url

    host = request.get_host()
    if host.startswith("127.0.0.1"):
        host = host.replace("127.0.0.1", "localhost")

    return f"{request.scheme}://{host}"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = (
            f"{get_backend_url(request)}"
            "/api/driveease/auth/google/callback/"
        )
        
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
            # Always show Google's account chooser so each browser context
            # can deliberately sign in with a different Google account.
            "prompt": "select_account consent",
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

        redirect_uri = (
            f"{get_backend_url(request)}"
            "/api/driveease/auth/google/callback/"
        )

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
                logger.warning("Google OAuth state validation failed")
                return redirect(f"{frontend_url}/client/login?error=oauth_failed")
        else:
            logger.warning("Google OAuth callback did not include state")
            return redirect(f"{frontend_url}/client/login?error=oauth_failed")

        try:
            token_response = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code',
                },
                timeout=15,
            )
            token_res = token_response.json()

            if 'access_token' not in token_res:
                logger.error(
                    "Google OAuth token exchange failed: status=%s error=%s description=%s redirect_uri=%s",
                    token_response.status_code,
                    token_res.get('error'),
                    token_res.get('error_description'),
                    redirect_uri,
                )
                return redirect(f"{frontend_url}/client/login?error=oauth_failed")

            profile_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={
                    'Authorization': f"Bearer {token_res['access_token']}"
                },
                timeout=15,
            )
            profile_res = profile_response.json()

            if not profile_response.ok:
                logger.error(
                    "Google OAuth profile request failed: status=%s error=%s",
                    profile_response.status_code,
                    profile_res.get('error'),
                )
                return redirect(f"{frontend_url}/client/login?error=oauth_failed")

            if not is_authorized(profile_res):
                return redirect(f"{frontend_url}/client/login?error=unauthorized")

            google_email = profile_res["email"].strip().lower()
            auth_user, created = User.objects.get_or_create(
                username=google_email,
                defaults={
                    "email": google_email,
                    "first_name": profile_res.get("given_name", ""),
                    "last_name": profile_res.get("family_name", ""),
                    "profile_picture": profile_res.get("picture", ""),
                }
            )

            if not created:
                updated_fields = []
                google_profile_fields = {
                    "first_name": profile_res.get("given_name", ""),
                    "last_name": profile_res.get("family_name", ""),
                    "profile_picture": profile_res.get("picture", ""),
                }
                for field, google_value in google_profile_fields.items():
                    if not getattr(auth_user, field) and google_value:
                        setattr(auth_user, field, google_value)
                        updated_fields.append(field)

                if updated_fields:
                    auth_user.save(update_fields=updated_fields)

            # Never issue a new session for an account suspended by an admin.
            if not auth_user.is_active:
                response = redirect(
                    f"{frontend_url}/client/login?error=suspended"
                )
                return delete_refresh_cookie(response)

            refresh = RefreshToken.for_user(auth_user)

            if auth_user.is_staff:
                response = redirect(f"{frontend_url}/admin/admin-dashboard/")
                return set_refresh_cookie(response, refresh)

            response = redirect(f"{frontend_url}/")
            return set_refresh_cookie(response, refresh)

        except Exception:
            logger.exception("Unexpected error while completing Google OAuth callback")
            return redirect(f"{frontend_url}/client/login?error=oauth_failed")

class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "user_reference": user.user_reference,
            "username": user.username,
            "given_name": user.first_name,
            "family_name": user.last_name,
            "email": user.email,

            "contact_number": user.contact_number,
            "address": user.address,
            "profile_picture": user.profile_picture,
            "id_images": user.id_images,

            "date_created": user.date_joined.isoformat(),
            "date_joined": user.date_joined.isoformat(),
            "status": "Active" if user.is_active else "Suspended",
            "role": get_account_role(user),
            "rentals": user.bookings.count(),
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

        submitted_id_images = data.get("id_images", user.id_images)
        submitted_images = (
            submitted_id_images.get("images")
            if isinstance(submitted_id_images, dict)
            else None
        )
        if not isinstance(submitted_images, list):
            return Response(
                {"id_images": "ID documents must be provided as a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(submitted_images) > 5:
            return Response(
                {"id_images": "A maximum of five ID documents is allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.id_images = {"images": submitted_images}

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

        # TokenRefreshSerializer does not reject inactive users by itself.
        # Check the account before rotating the cookie so a suspended account
        # cannot keep creating valid access tokens from an existing session.
        try:
            token = RefreshToken(refresh_token)
            user_id_claim = settings.SIMPLE_JWT.get(
                "USER_ID_CLAIM",
                "user_id",
            )
            user = User.objects.filter(pk=token.get(user_id_claim)).first()
        except TokenError:
            user = None

        if user is not None and not user.is_active:
            response = Response(
                {
                    "detail": "Your account has been suspended.",
                    "code": "account_suspended",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            return delete_refresh_cookie(response)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            # A revoked, expired, or malformed refresh token is an
            # authentication failure, not an application error. In
            # particular, token rotation can make a concurrently reused
            # token hit this path.
            return Response(
                {"detail": "Refresh token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

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
