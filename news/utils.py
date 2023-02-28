from datetime import datetime, timedelta, timezone
from news.models import Articles, LastNewsUpdate
from django.utils import timezone
import random
import urllib.request
import json


def retrieve_articles():
    try:
        last_update = LastNewsUpdate.objects.all()[0].time.date()
    except:
        last_update = timezone.now().date() - timedelta(days=30)

    if last_update < timezone.now().date():
        apikey = '55e35e8293000db759d15c226753cbd8'
        categories = ['world', 'technology', 'entertainment']

        for category in categories:
            api = f'https://gnews.io/api/v4/top-headlines?category={category}&lang=en&max=10&apikey={apikey}'
            response = urllib.request.urlopen(api)
            data = json.loads(response.read().decode('utf-8'))
            articles = data['articles']

            for article in articles:
                source = article['source']['name']
                title = article['title']
                description = article['description']
                url = article['url']
                image = article['image']

                pubdate = article['publishedAt'].split('T')[0].split('-')
                [year, month, day] = [int(pubdate[0]), int(pubdate[1]), int(pubdate[2])]
                date = datetime(year, month, day)

                if Articles.objects.filter(url=url).exists():
                    continue
                else:
                    try:
                        article_obj = Articles(
                            source=source,
                            title=title,
                            description=description,
                            url=url,
                            image=image,
                            date=date,
                            category=category
                        )
                        article_obj.save()
                    except:
                        continue

        if LastNewsUpdate.objects.exists():
            LastNewsUpdate.objects.update(time=timezone.now())
        else:
            initial_retrieve = LastNewsUpdate(time=timezone.now())
            initial_retrieve.save()

    current_articles = Articles.objects.filter(when_added=timezone.now().date())
    article_list = []
    for obj in current_articles:
        article_list.append(obj)

    articles_to_render = random.choices(article_list, k=3)

    return articles_to_render