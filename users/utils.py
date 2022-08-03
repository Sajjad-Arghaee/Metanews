from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
