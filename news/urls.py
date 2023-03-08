from django.urls import path
from news import views

app_name = 'browse'

urlpatterns = [
    path('search/', views.browse_search, name='search'),
    path('<category>/<uuid>/', views.article_detail, name='article'),
    path('<category>/', views.browse_view, name='category'),
    path('', views.browse_default)
]