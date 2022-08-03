from django.shortcuts import render, redirect
from .models import Profile, User, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomProfileCreationForm, CustomMessageForm
from .utils import paginate_posts


def show_profile(request, pk):
    profile = Profile.objects.get(name=pk)
    posts = profile.post_set.all()
    custom_range, posts = paginate_posts(request, posts, 6)
    context = {'profile': profile, 'posts': posts, 'custom_range': custom_range}
    return render(request, 'users/account.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('account')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'], password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('account')

        print('wrong password or username !')
    return render(request, 'users/login.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('account')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('account')
        else:
            print('something went wrong!')
    form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login_user')
def account(request):
    profile = request.user.profile
    posts = profile.post_set.all()
    custom_range, posts = paginate_posts(request, posts, 6)
    context = {'profile': profile, 'posts': posts, 'custom_range': custom_range}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = CustomProfileCreationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    form = CustomProfileCreationForm(instance=profile)
    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)


@login_required(login_url='login')
def send_message(request, pk):
    if request.method == 'POST':
        sender = request.user.profile
        receiver = Profile.objects.get(name=pk)
        form = CustomMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver
            message.save()
            return redirect('account')
    form = CustomMessageForm()
    context = {'form': form}
    return render(request, 'users/send-message.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messages = profile.messages.all()
    read_messages = []
    unread_messages = []
    unread_count = 0
    for message in messages:
        if message.seen:
            read_messages.append(message)
        else:
            unread_messages.append(message)
            unread_count += 1
    context = {'read_messages': read_messages, 'unread_messages': unread_messages, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def read_message(request, pk):
    message = Message.objects.get(id=pk)
    if not message.seen:
        message.seen = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)
