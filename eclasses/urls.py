"""eclasses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from users.views import GoogleAuthorizationAPIView, GoogleLogoutAPIView, GetCurrentUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('django.contrib.auth.urls')),
    path('api/auth/user/', GetCurrentUser.as_view(), name='current_user'),
    path('api/auth/google/', GoogleAuthorizationAPIView.as_view(), name='google_login'),
    path('api/auth/google/logout/', GoogleLogoutAPIView.as_view(), name='google_logout'),
    path('api/english/', include('english.urls')),
    path('docs/', get_swagger_view(title='EClasses Rest API Document')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
