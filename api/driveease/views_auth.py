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
from .models import UserProfile

from .utils.auth import is_authorized

from rest_framework_simplejwt.authentication import JWTAuthentication


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
            return redirect(f"{frontend_url}/login?error=cancelled")

        # Missing code
        if not code:
            return redirect(f"{frontend_url}/login?error=no_code")
            
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        secret = os.getenv("AUTH_SECRET", getattr(settings, 'AUTH_SECRET', ''))
        
        frontend_url = get_frontend_url()
        redirect_uri = f"{get_backend_url(request)}/api/driveease/auth/google/callback/"

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
            # Exchange auth code for access token
            token_res = requests.post('https://oauth2.googleapis.com/token', data={
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }).json()
            
            if 'access_token' not in token_res:
                return redirect(f"{frontend_url}/login?error=oauth_failed")
                
            # Get user profile
            profile_res = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={
                'Authorization': f"Bearer {token_res['access_token']}"
            }).json()
            
            if not is_authorized(profile_res):
                return redirect(f"{frontend_url}/login?error=unauthorized")
                
            user, _ = User.objects.get_or_create(
                username=profile_res.get('email'),
                defaults={
                    "email": profile_res.get('email'),
                    "first_name": profile_res.get('given_name', ''),
                    "last_name": profile_res.get('family_name', '')
                }
            )

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # attach google data into JWT
            access["given_name"] = profile_res.get("given_name")
            access["family_name"] = profile_res.get("family_name")
            access["email"] = profile_res.get("email")
            access["picture"] = profile_res.get("picture")

            access_token = str(access)

            # redirect to frontend
            return redirect(f"{frontend_url}/?token={access_token}")
            
        except Exception as e:
            return redirect(f"{frontend_url}/login?error=oauth_failed")

class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        return Response({
            "id": request.user.id,
            "given_name": request.auth.get("given_name"),
            "family_name": request.auth.get("family_name"),
            "email": request.auth.get("email"),
            "picture": request.auth.get("picture"),
            "date_joined": request.user.date_joined.isoformat(),

            "contact_number": profile.contact_number,
            "address": profile.address,
            "profile_picture": request.build_absolute_uri(profile.profile_picture.url) if profile.profile_picture else None,
            "license_image": request.build_absolute_uri(profile.license_image.url) if profile.license_image else None,
            "id_image": request.build_absolute_uri(profile.id_image.url) if profile.id_image else None,
        })

class AuthLogoutView(APIView):
    def post(self, request):
        return Response({"status": "logged_out"})