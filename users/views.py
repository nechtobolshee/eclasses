import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from eclasses.settings import ALLOWED_EMAIL_DOMAINS
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User

from .serializers import UserDetailsSerializer


class GetCurrentUser(RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch']
    authentication_classes = (TokenAuthentication, SessionAuthentication, JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj


class GoogleAuthorizationAPIView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            return Response({'message': 'Wrong google token / this google token is already expired.'})

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            if data['email'].split('@')[-1] not in ALLOWED_EMAIL_DOMAINS:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data="Not allowed e-mail domain. Please, use another e-mail.")
            else:
                user = User()
                user.username = data['email'].split('@')[0]
                user.password = make_password(BaseUserManager().make_random_password())
                user.email = data['email']
                user.save()

        token = RefreshToken.for_user(user)
        return Response(
            {
                'username': user.username,
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
        )


class GoogleLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
