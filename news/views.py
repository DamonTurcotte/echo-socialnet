from django.shortcuts import render
from django.urls import reverse
from news.models import Articles
from django.utils import timezone
from django.http import HttpResponseRedirect
import random

articles = Articles.objects.filter(when_added=timezone.now().date())

categories = {
    'world': articles.filter(category='world'),
    'tech': articles.filter(category='technology'),
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

    article = Articles.objects.get(uuid=uuid)

    context = {
        'title': f'{category.capitalize()} | Echo',
        'article': article
    }

    return render(request, 'news/article.html', context=context)