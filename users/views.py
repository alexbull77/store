from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import User


class UserRegistrationView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Store - Регистрация'
        return context


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserLoginForm(data=request.POST)
        # audit (контроль)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authentification (подтверждение подлинности)
            user = auth.authenticate(username=username, password=password)
                # authorisation (разрешение)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'users/login.html', context={'form': form})
    else:
        return render(request,
                      'users/login.html',
                      context={'form': UserLoginForm()})


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Store - Профиль'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
