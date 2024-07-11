from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



# Create your views here.
class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:index')
        return render(request, self.template_name, {'form': form})


def profile(request):
    return HttpResponse('you logged in')


def log_out(request):
    logout(request)
    return HttpResponse('you logged out')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form=UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
    context={
        'user_form':user_form,
    }
    return render(request, 'registration/edit_user.html',context)