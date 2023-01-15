from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import (UserLoginView, UserLogoutView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', login_required(UserLogoutView.as_view()), name='logout'),
]
