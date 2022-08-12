from django.shortcuts import render, redirect
from .models import Post, TagVisit, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from interface.utils import paginate_posts
from monkeylearn import MonkeyLearn
import pandas as pd
import numpy as np
from math import sqrt


def show_post(request, pk):
    post = Post.objects.get(title=pk)
    post.views_count += 1
    post.save()
    if request.user.is_authenticated:
        profile = request.user.profile
        tags = post.tags.all()
        for tag in tags:
            t, created = TagVisit.objects.get_or_create(name=tag.name, profile_id=profile.id)
            if not created:
                t.count += 1
                t.save()

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
            ml = MonkeyLearn('4201683e97f0c1d475d3a466097c0e63e8082c54')
            data = [post.title]
            model_id = 'ex_YCya9nrn'
            result = ml.extractors.extract(model_id, data)
            data_dict = result.body
            extracted_tags = []
            for item in data_dict[0]['extractions'][:5]:
                line = item['parsed_value'].split()
                extracted_tags.extend(line)
            print(extracted_tags)
            for tag in extracted_tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                t = Tag.objects.get(name=tag)
                p = Post.objects.get(title=post.title)
                p.tags.add(t)
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


def suggest_post(request):
    # content based learning
    profile = request.user.profile
    tags_visited = profile.tagvisit_set.filter(profile_id=profile.id)[:50]
    all_posts = Post.objects.all()[:50]
    if tags_visited:
        posts_score = [[0, x] for x in range(len(all_posts))]

        # collaborative based leaning
        other_tags_visited = []
        for tag in tags_visited:
            other_tags_visited_copy = TagVisit.objects.filter(name=tag.name)
            for t in other_tags_visited_copy:
                if t.profile_id != profile.id:
                    other_tags_visited.append(t)
        df_other_tags_visited = pd.DataFrame(other_tags_visited)
        df_other_tags_visited.columns = [['name']]
        df_other_tags_visited['name'] = df_other_tags_visited['name'].astype(str)
        df_other_tags_visited['id'] = [tag.profile_id for tag in other_tags_visited]
        df_other_tags_visited['count'] = [tag.count for tag in other_tags_visited]
        df_other_tags_visited = pd.DataFrame(df_other_tags_visited.values, columns=['name', 'id', 'count'])
        users_group = df_other_tags_visited.groupby(by=['id'])
        users_group = sorted(users_group, key=lambda x: len(x[1]), reverse=True)
        # applying pearson correlation
        pearson_correlation_dict = dict()
        for name, group in users_group:
            group = group.sort_values(by='name')
            input_tags = pd.DataFrame(tags_visited.values())
            input_tags = input_tags.sort_values(by='name')
            input_tags['id'] = input_tags['profile_id']
            input_tags = input_tags.drop('profile_id', axis=1)
            input_tags = input_tags[input_tags['name'].isin(group['name'].tolist())]
            n = len(group)
            input_count_list = input_tags['count'].tolist()
            group_count_list = group['count'].tolist()
            sxx = sum([i ** 2 for i in input_count_list]) - pow(sum(input_count_list), 2) / float(n)
            syy = sum([i ** 2 for i in group_count_list]) - pow(sum(group_count_list), 2) / float(n)
            sxy = sum(i * j for i, j in zip(input_count_list, group_count_list)) - sum(input_count_list) * sum(
                group_count_list) / float(n)

            # If the denominator is different than zero, then divide, else, 0 correlation.
            if sxx != 0 and syy != 0:
                pearson_correlation_dict[name] = sxy / sqrt(sxx * syy)
            else:
                pearson_correlation_dict[name] = 0

        pearson_df = pd.DataFrame.from_dict(pearson_correlation_dict, orient='index')
        pearson_df.columns = ['similarityIndex']
        pearson_df['id'] = pearson_df.index
        pearson_df.index = range(len(pearson_df))
        pearson_df = pearson_df.sort_values(by='similarityIndex', ascending=False)
        top_tags = pearson_df.merge(df_other_tags_visited, left_on='id', right_on='id', how='inner')
        top_tags['weightedCount'] = top_tags['similarityIndex'] * top_tags['count']
        top_tags_copy = top_tags
        top_tags_copy['similarityIndex'] = top_tags['weightedCount']
        temp_top_tags = top_tags.groupby('name')
        temp_top_tags = temp_top_tags.sum()[['similarityIndex']]
        temp_top_tags.columns = ['sum_similarityIndex']
        temp_top_tags2 = top_tags.groupby('name')
        temp_top_tags2 = temp_top_tags2.sum()[['similarityIndex']]
        temp_top_tags2.columns = ['sum_similarityIndex']
        temp_top_tags['sum_weightedCount'] = temp_top_tags2['sum_similarityIndex']
        recommendation_df = pd.DataFrame()
        recommendation_df['weighted average recommendation score'] = (temp_top_tags['sum_weightedCount']+1) / (temp_top_tags['sum_similarityIndex']+1)
        recommendation_df['name'] = temp_top_tags.index
        recommendation_df.index = range(len(recommendation_df))
        recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
        collaborative_result = recommendation_df[['name', 'weighted average recommendation score']].to_numpy()

        for i in range(len(all_posts)):
            for tag in tags_visited:
                if tag.name in all_posts[i].title:
                    posts_score[i][0] += tag.count
            posts_score[i][0] += all_posts[i].views_count / 2
        for i in range(len(all_posts)):
            for tag in collaborative_result:
                if tag[0] in all_posts[i].title:
                    posts_score[i][0] += tag[1]

        posts_score = sorted(posts_score, reverse=True)[:50]
        print(posts_score)
        selected_posts = []
        for counter, index in posts_score:
            selected_posts.append(all_posts[index])
    else:
        selected_posts = all_posts
    custom_range, posts = paginate_posts(request, selected_posts, 9)
    context = {'posts': posts, 'custom_range': custom_range}
    return render(request, 'interface/suggest.html', context)
