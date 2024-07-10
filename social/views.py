from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import *
from django.http import HttpResponse


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