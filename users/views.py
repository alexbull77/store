from django.contrib import auth, messages
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'users/register.html', context={'form': form})
    else:
        return render(request,
                      'users/register.html',
                      context={'form': UserRegistrationForm()})

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

def profile(request):
    if request.method == 'POST': 
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            return render(request, 'users/error.html', context={'form': form})
    else:
        return render(request,
                      'users/profile.html',
                      context={'title': 'Store - Профиль',
                               'form': UserProfileForm(instance=request.user)
                              })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))