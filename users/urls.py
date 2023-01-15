from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import UserProfileView, UserRegistrationView, login, logout

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout'),
]
