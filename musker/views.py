from django.shortcuts import render, redirect
from .models import Profile, Meep
from django.contrib import messages
from .forms import MeepForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False) 
                meep.user = request.user
                meep.save()
                messages.success(request, ('You Meep has been posted'))
                return redirect('home')
            
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"meeps":meeps, "form":form})
    else:
        
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"meeps":meeps})
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page...'))
        return redirect('home')


def profile(request, pk):

    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        meeps = Meep.objects.filter(user_id = pk).order_by('-created_at')  # Get all meeps from this profile

        # Post Form logic
        if request.method=="POST":
            # Get current user ID
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST["follow"]
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":  
                current_user_profile.follows.add(profile)
            # Save profile
            current_user_profile.save()


        return render(request, "profile.html", {"profile":profile, "meeps":meeps})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page...'))
        return redirect('home')

def login_user(request):
    return render(request, "login.html", {})


def logout_user(request):
    pass
