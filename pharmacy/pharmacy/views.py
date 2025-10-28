from django.shortcuts import render

def home(request):
    context = {
        "home_page":"Home page 123",
        "user_name":"Damian"
    }
    
    return render(request, "home.html", context)

from django.shortcuts import render

def about(request):
    context = {
        "about_page": "About page 123",
        "user_name": "Damian"
    }
    return render(request, 'about.html', context)