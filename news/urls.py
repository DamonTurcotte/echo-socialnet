from django.urls import path
from news import views

urlpatterns = [
    path('<category>/<uuid>/', views.article_detail, name='article'),
    path('<category>/', views.browse_view, name='browse'),
    path('', views.browse_default)
]