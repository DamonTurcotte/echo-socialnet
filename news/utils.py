from datetime import datetime, timedelta, timezone
from news.models import Articles, LastNewsUpdate
from django.utils import timezone
import random
import urllib.request
import json
import re


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

                # if content is truncated, remove trunc. tag from content string
                content_str = str(article['content'])
                if re.search('\\[[0-9]*\\s*chars\\]', content_str):
                    regex = re.search('\\[[0-9]*\\s*chars*\\]', content_str)
                    pos = regex.start()#type:ignore
                    content_str = content_str[:pos]
                content = content_str

                pubdate = article['publishedAt'].split('T')[0].split('-')
                [year, month, day] = [int(pubdate[0]), int(pubdate[1]), int(pubdate[2])]
                date = datetime(year, month, day)

                if Articles.objects.filter(title=title).exists() or Articles.objects.filter(url=url).exists():
                    continue
                else:
                    try:
                        article_obj = Articles(
                            source=source,
                            title=title,
                            description=description,
                            content=content,
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

    articles_to_render = []
    i = 0
    while i < 3:
        try:
            rand_article = random.choice(article_list)
            articles_to_render.append(rand_article)
            article_list.remove(rand_article)
            i += 1
        except: break

    return articles_to_render