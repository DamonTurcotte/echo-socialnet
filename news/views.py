from django.shortcuts import render
from django.urls import reverse
from news.models import Articles
from django.utils import timezone
from django.http import HttpResponseRedirect
from posts.models import Post
from django.db.models import Count
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
    return HttpResponseRedirect(reverse('browse', args=[category]))

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