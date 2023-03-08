from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from news.models import Articles
from posts.models import Post
from users.models import EchoUser
from django.db.models import Count, Q
import random

articles = Articles.objects.filter(when_added=timezone.now().date())

categories = {
    'world': articles.filter(category='world'),
    'technology': articles.filter(category='technology'),
    'entertainment': articles.filter(category="entertainment")
}

def browse_view(request, category):

    context = {
        'title': 'Browse | Echo',
        'articles': categories[category]
    }

    return render(request, 'news/browse.html', context=context)

def browse_default(request):
    category = random.choice(list(categories.keys()))
    return HttpResponseRedirect(reverse('browse:category', args=[category]))

def article_detail(request, category, uuid):
    if request.method == 'POST':
        post = request.POST['post']
        user = request.user
        article = Articles.objects.get(uuid=uuid)

        if request.POST['type'] == 'comment':
            comment = Post(article_comment=article, echouser=user, post=post)
            comment.save()

        if request.POST['type'] == 'share':
            share = Post(article_share=article, echouser=user, post=post)
            share.save()

    article = Articles.objects.get(uuid=uuid)
    # order article comments by total user interactions with comment

    if Post.objects.filter(article_comment=article).exists():

        comments = Post.objects.filter(
            article_comment=article).annotate(count=(
            Count('likes') + Count('replies') + Count('reposts'))).order_by(
            'count').reverse()

        comment_list = []
        for comment in comments:
            comment_detail = {'details': comment, 'liked': ''}

            if request.user.is_authenticated:
                if comment.likes.filter(uuid=request.user.uuid).exists():
                    comment_detail['liked'] = ' active'

            comment_list.append(comment_detail)

    else: comment_list = None

    context = {
        'title': f'{category.capitalize()} | Echo',
        'article': article,
        'comments': comment_list
    }

    return render(request, 'news/article.html', context=context)


def browse_search(request):
    query = request.GET.get('q')

    if query:
        [user_list, post_list, article_list] = [[], [], []]

        user_results = EchoUser.objects.filter(username__icontains=query).annotate(
            follower_count=Count('followers')).order_by('follower_count').reverse()
        
        post_results = Post.objects.filter(post__icontains=query).annotate(
            popularity=(Count('likes') + Count('reposts') + Count('replies'))).order_by('popularity').reverse()
        
        article_results = Articles.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)).annotate(
            popularity=(Count('article_comments') + Count('article_shares'))).order_by('popularity').reverse()

        for result in user_results:
            if len(user_list) < 9:
                user = dict()
                user['username'] = result.username
                user['avatar'] = result.avatar.url
                user['uuid'] = result.uuid
                user_list.append(user)

            else: break

        for result in post_results:
            if len(post_list) + len(user_list) < 9:
                post = dict()
                post['uuid'] = result.uuid
                post['username'] = result.echouser.username
                post['avatar'] = result.echouser.avatar.url
                post['content'] = result.post
                post_list.append(post)

            elif len(post_list) < 4:
                post = dict()
                post['uuid'] = result.uuid
                post['username'] = result.echouser.username
                post['avatar'] = result.echouser.avatar.url
                post['content'] = result.post
                post_list.append(post)
                user_list.pop()

            else: break
        
        for result in article_results:
            if len(article_list) + len(post_list) + len(user_list) < 9:
                article = dict()
                article['uuid'] = result.uuid
                article['category'] = result.category
                article['title'] = result.title[:40]
                article['source'] = result.source[:30]
                article_list.append(article)

            elif len(article_list) < 3:
                article = dict()
                article['uuid'] = result.uuid
                article['category'] = result.category
                article['title'] = result.title[:40]
                article['source'] = result.source[:30]
                article_list.append(article)

                if len(user_list) > len(post_list):
                    user_list.pop()
                elif len(post_list) >= len(user_list):
                    post_list.pop()

            else: break

        data = {
            'users': user_list,
            'posts': post_list,
            'articles': article_list
            }

        return JsonResponse(data)
    
    else: return render(request, '404.html')