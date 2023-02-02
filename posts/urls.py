from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('newpost/', views.create_post, name='create_post'),
    path('<uuid>/', views.post_detail_view, name='post_detail')
]