from django.urls import path, include
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
)
from dj_rest_auth.registration.views import RegisterView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    UserProfileView,
    GenreListView,
    UpdateFavoriteGenresView,
    ChangePasswordView,
    UploadAvatarView
)

# Google OAuth2 Login View
# For REST API: Frontend gets access_token from Google, then sends it here
# Use default serializer from dj_rest_auth which handles everything properly
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = None  # Not needed for REST API
    client_class = OAuth2Client
    # use default serializer from dj_rest_auth


urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserDetailsView.as_view(), name="user"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Social Login
    path("google/", GoogleLogin.as_view(), name="google_login"),

    # JWT Endpoints
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),

    # Password Management
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),

    # Profile & Avatar
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/avatar/", UploadAvatarView.as_view(), name="upload-avatar"),

    # Genres
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("profile/genres/", UpdateFavoriteGenresView.as_view(), name="update-genres"),
]
