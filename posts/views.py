from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def show_post(request, pk):
    post = Post.objects.get(title=pk)
    post.views_count += 1
    post.save()
    context = {'post': post}
    return render(request, 'posts/single-post.html', context)


@login_required(login_url='login')
def add_post(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile
            profile.active_posts += 1
            post.save()
            profile.save()
            return redirect('account')
    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/post-form.html', context)


@login_required(login_url='login')
def update_post(request, pk):
    post = Post.objects.get(title=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('account')
    form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/post-form.html', context)


@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(title=pk)
    if request.method == 'POST':
        post.delete()
        profile = post.author
        profile.active_posts -= 1
        profile.save()
        return redirect('account')
    else:
        return render(request, 'posts/delete_template.html', {'post': post})
