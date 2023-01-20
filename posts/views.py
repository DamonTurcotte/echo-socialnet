from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Post



def create_post(request):
    if request.method == 'POST':
        post = request.POST['post']
        echouser = request.user
        try:
            reply_to = request.POST['reply_to']
            reply_to = Post.objects.get(uuid=reply_to)
            Post.objects.create(post=post, echouser=echouser, reply_to=reply_to)
            return redirect(request.POST['newpath'])
        except:
            Post.objects.create(post=post, echouser=echouser)
            return redirect(reverse('home'))
    
    context = {
        'title': 'New Post | Echo',
    }
    return render(request, 'posts/create_post.html', context=context)


def create_reply(request):
    if request.method == 'POST':
        post = request.POST['post']
        reply_to = request.POST['reply_to']
        echouser = request.user
        Post.objects.create(post=post, reply_to=reply_to, echouser=echouser)

        data = {}

        return JsonResponse(data)
    
    else: return render(request, '404.html')


