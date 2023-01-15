from common.views import TitleMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    title = 'Store - Регистрация'
    success_message = 'Congratulations!'


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = "users/email_verification.html"
    title = 'Store Email Verification'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(
            user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
