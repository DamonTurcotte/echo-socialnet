from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post


def create_post(request):
    if request.method == 'POST':
        post = request.POST['post']
        echouser = request.user
        Post.objects.create(post=post, echouser=echouser)
        
        return redirect(reverse('home'))
        

    context = {
        'title': 'New Post | Echo',
    }
    return render(request, 'posts/create_post.html', context=context)
