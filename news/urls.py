from django.urls import path
from news import views

app_name = 'browse'

urlpatterns = [
    path('search/<category>/', views.browse_search_results, name='search'),
    path('search/', views.browse_search),
    path('<category>/<uuid>/', views.article_detail, name='article'),
    path('<category>/', views.browse_view, name='category'),
    path('', views.browse_default)
]