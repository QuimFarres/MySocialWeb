from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, UserProfile
from django.core.paginator import Paginator


@login_required(login_url='signin')
def index(request):
    # Retrieve all posts
    posts = Post.objects.all().order_by('-created_at')

    # Set the number of posts to display per page
    tweet_count = request.GET.get('tweet_count', 10)
    paginator = Paginator(posts, tweet_count)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page of posts
    page_obj = paginator.get_page(page_number)

    following = request.user.following.all()  # Get users the user is following

    context = {
        'posts': page_obj,
        'total_tweets': paginator.count,
        'tweet_count': int(tweet_count),
        'following': following,
    }
    return render(request, 'index.html', context)




@login_required(login_url='login')  # Redirects to the login page if the user is not logged in
def create_post(request):
    if request.method == 'POST':
        user = request.user  # Retrieve the authenticated user
        text = request.POST['text']
        created_at = timezone.now()

        post = Post.objects.create(user=user, text=text, created_at=created_at)
        post.save()

        return redirect('index')
    else:
        return render(request, 'index.html')

@login_required(login_url='login')
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('index')

@login_required
def add_comment(request, tweet_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            tweet = Post.objects.get(pk=tweet_id)
            comment = Comment.objects.create(user=request.user, text=text)
            tweet.comments.add(comment)
    return redirect('index')

@login_required
def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
        else:
            comment.liked_by.add(user)
    return redirect('index')


@login_required
def follow_user(request, user_id):
    if request.method == 'POST':
        user_to_follow = UserProfile.objects.get(user_id=user_id)
        request.user.userprofile.following.add(user_to_follow.user)
        return redirect('index')  # Redirect to the feed after following

@login_required
def unfollow_user(request, user_id):
    if request.method == 'POST':
        user_to_unfollow = UserProfile.objects.get(user_id=user_id)
        request.user.userprofile.following.remove(user_to_unfollow.user)
        return redirect('index')  # Redirect to the feed after unfollowing

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Create a UserProfile instance for the new user
                user_profile = UserProfile.objects.create(user=user)

                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:  #exists
            auth.login(request, user)
            return redirect('/')
        else:                  #dosnt exist
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        print(user)

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        print('redirected no POST')
        return redirect('/')
    
