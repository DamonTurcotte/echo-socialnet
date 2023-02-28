from users.models import EchoUser
from news.utils import retrieve_articles


# installed in settings.py as echo.context_processors.add_variable_to_base
def add_variable_to_base(request):
    new_users_query = EchoUser.objects.order_by('date_joined').reverse().all()[0:3]
    new_users = []
    i = 0
    for user in new_users_query:
        i += 1
        new_users.append(user)

    articles = retrieve_articles()

    return {'new_users': new_users, 'side_articles': articles}

    