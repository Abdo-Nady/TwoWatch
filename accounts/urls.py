from django.urls import path, include
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
)
from dj_rest_auth.registration.views import RegisterView

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

urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserDetailsView.as_view(), name="user"),
    path("logout/", LogoutView.as_view(), name="logout"),

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
