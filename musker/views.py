from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Meep
from django.contrib import messages
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
    if request.method == "POST":   
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in succesesfully! Get Meeping"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please try again"))
            return redirect('login')
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered! Welcome"))

            return redirect('home')
    
    return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id = current_user.id)

        # Get forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance = current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None,   instance = profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save() 
            messages.success(request, ('Your Information has been updated successfully'))
            login(request, current_user)
            return redirect('home')
        return render(request, "update_user.html", {"user_form":user_form, "profile_form":profile_form})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page...'))
        return redirect('home')


def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You Must Be Logged In To View This Page...'))
        return redirect('home')

def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'meep_show.html', {'meep':meep})

    else:
        messages.success(request, ('That meep does not exist...'))
        return redirect('home')