"""jwt_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from jwtapi import views as jwtapi_views  
from ProfilePost import views as profile_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", jwtapi_views.logout_user, name="logout"),
    path("register/", jwtapi_views.user_register_view, name="register"),
    path("profile/", profile_views.ProfileListeCreateView.as_view(), name="profile"),
    path("posts/", profile_views.PostListeCreateView.as_view(), name="post"),
    path("posts/<int:pk>/", profile_views.PostDetailView.as_view(), name="post_view"),
    path("posts/<int:pk>/comment", profile_views.CommentListeCreateView.as_view(), name="comment"),
]
