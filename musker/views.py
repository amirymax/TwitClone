from django.shortcuts import render, redirect
from .models import Profile 
from django.contrib import messages
def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page...'))
        return redirect('home')