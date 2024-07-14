from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm, SignUpForm, UserUpdateForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("Your tweet has been posted!"))
                return redirect('twitter:home')
            
        tweets = Tweet.objects.all().order_by('-created_at')
        context = {'tweets': tweets,
                   'form': form,
                    }
        return render(request, 'home.html', context=context)
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
        context = {'tweets': tweets}
        return render(request, 'home.html', context=context)

def profile_list(request):
    if request.user.is_authenticated:
        # exclude the logged in user profile
        profiles = Profile.objects.exclude(user=request.user)
        context = {'profiles': profiles}
        return render(request, 'profile_list.html', context=context)
    else:
        messages.error(request, ("You must be logged in!"))
        return redirect('twitter:home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-created_at')
        
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()

        context = {
                    'profile': profile,
                    'tweets': tweets,
                }
        return render(request, 'profile.html', context=context)
    else:
        messages.error(request, ("You must be logged in!"))
        return redirect('twitter:home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=pk)
            user_follows = request.user.profile.follows.all()

            if profile in user_follows:
                # unfollow the user
                request.user.profile.follows.remove(profile)
                # save the changes to your profile
                request.user.profile.save()
                messages.success(request, (f'You unfollowed @{profile.user.username}'))
            else:
                messages.error(request, ('Invalid request!'))
            
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            return redirect('twitter:profile', pk=request.user.id)
    else:
        messages.error(request, ('You must be logged in!'))
        return redirect('twitter:home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=pk)
            user_follows = request.user.profile.follows.all()

            if not profile in user_follows:
                # follow the user
                request.user.profile.follows.add(profile)
                # save the changes to your profile
                request.user.profile.save()
                messages.success(request, (f'You followed @{profile.user.username}'))
            else:
                messages.error(request, ('Invalid request!'))
            
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            return redirect('twitter:profile', pk=request.user.id)
    else:
        messages.error(request, ('You must be logged in!'))
        return redirect('twitter:home')
    
def remove_follower(request, pk):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=pk)
            user_followers = request.user.profile.followed_by.all()

            if profile in user_followers:
                # remove the user from my followers list
                request.user.profile.followed_by.remove(profile)
                # save the changes to your profile
                request.user.profile.save()
                messages.success(request, (f'You removed @{profile.user.username} from your followers!'))
            else:
                messages.error(request, ('Invalid request!'))
            
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            return redirect('twitter:profile', pk=request.user.id)
    else:
        messages.error(request, ('You must be logged in!'))
        return redirect('twitter:home')
    
def followers(request, pk):
    if request.user.is_authenticated:
        # profile = Profile.objects.get(user_id=pk)
        profiles = Profile.objects.get(user_id=pk)
        if profiles.account_type == 'public':
            # public acc
            context = {'profiles': profiles}
            return render(request, 'followers.html', context=context)
        else:
            if request.user.id == pk:
                context = {'profiles': profiles}
                return render(request, 'followers.html', context=context)
            else:
                messages.error(request, ("You can\'t view this! It\'s a private account"))
                return redirect('twitter:profile', pk=profiles.user.pk)
    else:
        messages.error(request, ("You must be logged in!"))
        return redirect('twitter:home')
    
def following(request, pk):
    if request.user.is_authenticated:
        # profile = Profile.objects.get(user_id=pk)
        profiles = Profile.objects.get(user_id=pk)
        if profiles.account_type == 'public':
            # public acc
            context = {'profiles': profiles}
            return render(request, 'following.html', context=context)
        else:
            if request.user.id == pk:
                context = {'profiles': profiles}
                return render(request, 'following.html', context=context)
            else:
                messages.error(request, ("You can\'t view this! It\'s a private account"))
                return redirect('twitter:profile', pk=profiles.user.pk)
    else:
        messages.error(request, ("You must be logged in!"))
        return redirect('twitter:home')

def login_user(request):
    # if user already logged in redirect back to home
    if request.user.is_authenticated:
        return redirect('twitter:home')

    # login user
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('twitter:home')
        else:
            messages.error(request, "Wrong credentials! Try again")
            # Redirect back to login page with error message
            return redirect('twitter:login')
        
    # If request.method is not POST, render the login form
    return render(request, "login.html")

def logout_user(request):
    # if user not logged in redirect back to home page
    if not request.user.is_authenticated:
        return redirect('twitter:home')
    
    # if user logged in then logout
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('twitter:home')
    
def register_user(request):
    if request.user.is_authenticated:
        return redirect('twitter:home')
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered!"))
            return redirect('twitter:home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', context={'form': form})

@login_required
def update_user(request):
    current_user = request.user
    user_id = request.user.id
    profile_user = Profile.objects.get(user__pk=request.user.pk)
    
    form = UserUpdateForm(instance=current_user)
    profile_form = ProfilePicForm(instance=profile_user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST, request.FILES or None, instance=profile_user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('twitter:profile', pk=user_id)
        
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'update_user.html', context=context)

def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, pk=pk)
        if tweet.likes.filter(pk=request.user.pk):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)

        return redirect(request.META.get('HTTP_REFERER'))   

    else:
        messages.error(request, ("You must be logged in!"))
        return redirect('twitter:home')
    
def tweet_share(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet:
        context = {'tweet': tweet}
        return render(request, 'share_tweet.html', context=context)
    else:
        messages.error(request, ('This tweet doesn\'t exist!'))
        return redirect('twitter:home')
    
def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        # check tweet owner
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request, ('Your tweet has been deleted!'))
            return redirect('twitter:profile', pk=request.user.pk)
        else:
            messages.error(request, ('This action can\'t be performed!'))
            return redirect('twitter:home')
    else:
        messages.error(request, ('Please Log in to continue...'))
        return redirect('twitter:login')

def edit_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        form = TweetForm(request.POST or None, instance=tweet)
        # check tweet owner
        if request.user.username == tweet.user.username:
            if request.method == 'POST':
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, ('Your tweet has been updated'))
                    return redirect('twitter:home')
                # context is defined here
            context = {'form': form, 'tweet': tweet}
            return render(request, "edit_tweet.html", context=context)
        else:
            messages.error(request, ('This action can\'t be performed!'))
            return redirect('twitter:home')
    else:
        messages.error(request, ('Please Log in to continue...'))
        return redirect('twitter:login')
    
def search(request):
    if request.method == 'POST':
        # grab the form field input
        search = request.POST['search']
        # search the database
        searched = Tweet.objects.filter(body__icontains=search)
        context = {'search': search, 'searched': searched}
        return render(request, 'search.html', context=context)
    else:
        return render(request, 'search.html')

def search_user(request):
    if request.method == 'POST':
        # grab the form field input
        search = request.POST['search']
        # search the database
        searched = User.objects.filter(username__icontains=search)
        context = {'search': search, 'searched': searched}
        return render(request, 'search_user.html', context=context)
    else:
        return render(request, 'search_user.html')