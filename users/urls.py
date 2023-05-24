from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/<uuid>/', views.profile_view, name='profile'),
    path('user_data/', views.EchoUserResourceView.as_view(), name='user_data'),
]
