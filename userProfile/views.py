from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User


def sign_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('email').strip(), password=request.POST.get('password'))
        print(user)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('event')

    return render(request, 'org-admin/login.html', {})


def sign_out(request):
    logout(request)
    return render(request, 'org-admin/login.html', {})
