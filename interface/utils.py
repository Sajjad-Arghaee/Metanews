from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from posts.models import Post
from django.db.models import Q


def search_project(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    posts = Post.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(author__name__icontains=search_query)
    )

    return search_query, posts


def paginate_posts(request, posts, results):
    page = request.GET.get('page')
    paginator = Paginator(posts, results)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return custom_range, posts
