from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to home page
        else:
            return render(request, 'pharmacy/login.html', {'form': {'errors': True}})
    return render(request, 'pharmacy/login.html')
