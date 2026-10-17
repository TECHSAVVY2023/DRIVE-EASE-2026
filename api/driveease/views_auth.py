import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
import urllib.parse
import base64

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .utils.auth import is_authorized
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from .models import FileUploadModel

User = get_user_model()

def get_frontend_url():
    return os.getenv("FRONTEND_DRIVEEASE_URL", "http://localhost:3000").rstrip('/')

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
        
        origin = request.GET.get('origin', get_frontend_url())
        state_data = {
            'redirect_uri': redirect_uri,
            'frontend_url': origin.rstrip('/')
        }
        import json
        state = base64.b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')
        
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
                import json
                state_data = json.loads(base64.b64decode(state_param).decode('utf-8'))

                redirect_uri = state_data.get('redirect_uri', redirect_uri)
                frontend_url = state_data.get('frontend_url', frontend_url)

            except Exception:
                pass

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

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            if auth_user.is_staff:
                return redirect(
                    f"{frontend_url}/admin/admin-dashboard/?access={access_token}&refresh={refresh_token}"
                )

            return redirect(
                f"{frontend_url}/?access={access_token}&refresh={refresh_token}"
            )

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

        user.profile_picture = data.get(
            "profile_picture",
            user.profile_picture
        )

        user.id_images = data.get(
            "id_images",
            user.id_images
        )

        deleted_images = data.get("deleted_images", [])

        for upload in FileUploadModel.objects.all():

            if upload.file and upload.file.url in deleted_images:
                upload.file.delete(save=False)
                upload.delete()

        user.save()

        return Response({
            "message": "Profile updated successfully"
        })

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "No refresh token"}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data.get("refresh")
        })