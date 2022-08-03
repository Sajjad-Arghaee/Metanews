from django.shortcuts import render
from posts.models import Post
from users.models import Profile
from .utils import paginate_posts, search_project


def index(request):
    if request.GET.get('search_query'):
        search_query, posts = search_project(request)
        custom_range, posts = paginate_posts(request, posts, 9)
        context = {'search_query': search_query, 'posts': posts, 'custom_range': custom_range}
        return render(request, 'interface/index_search.html', context)

    profiles = Profile.objects.order_by('-active_posts')[0:6]
    posts = Post.objects.order_by('-views_count')[0:9]
    context = {'profiles': profiles, 'posts': posts}
    return render(request, 'interface/index.html', context)


def about(request):
    context = {}
    return render(request, 'interface/about.html', context)


def contact(request):
    context = {}
    return render(request, 'interface/contact.html', context)


def faq(request):
    context = {}
    return render(request, 'interface/faq.html', context)


def topic(request, pk):
    if pk:
        posts = Post.objects.filter(topic=pk)
        top_posts = posts.order_by('-views_count')[0:3]
        custom_range, posts = paginate_posts(request, posts, 9)
        context = {'topic': pk, 'posts': posts, 'top_posts': top_posts, 'custom_range': custom_range}
    else:
        context = {}
    return render(request, 'interface/topic.html', context)
