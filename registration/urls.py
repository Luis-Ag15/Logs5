from django.urls import path
from .views import (
    SignUpView,
    ProfileUpdate,
    EmailUpdate,
    UsernameUpdate,
    profile_qr
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileUpdate.as_view(), name="profile"),
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),
    path('profile/username/', UsernameUpdate.as_view(), name="profile_username"),
    path('profile/qr/', profile_qr, name="profile_qr"),
]

