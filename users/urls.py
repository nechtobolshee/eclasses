from django.urls import path, include
from .views import GoogleAuthorizationAPIView, GoogleLogoutAPIView, GetCurrentUserRetrieveUpdateAPIView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('user/', GetCurrentUserRetrieveUpdateAPIView.as_view(), name='current_user'),
    path('google/', GoogleAuthorizationAPIView.as_view(), name='google_login'),
    path('google/logout/', GoogleLogoutAPIView.as_view(), name='google_logout'),
]
