from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view),
    path('ajax/', views.chat_response, name='chat_ajax'),
    path('<uuid>/', views.message_view, name='message'),
]
