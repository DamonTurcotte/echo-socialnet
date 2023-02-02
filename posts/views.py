from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Post
from django.views.generic import DetailView
from echo.utils import make_post_objects



def create_post(request):
    if request.method == 'POST':
        post = request.POST['post']
        echouser = request.user

        try:
            try:
                repost_of = request.POST['repost_of']
                repost_of = Post.objects.get(uuid=repost_of)
                Post.objects.create(post=post, echouser=echouser, repost_of=repost_of)

                return redirect(request.POST['newpath'])

            except:
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


def post_detail_view(request, uuid):
    post_list = list()
    main_post = Post.objects.get(uuid=uuid)
    post_list.append(main_post)

    if main_post.reply_to != None:
        reply_to = main_post.reply_to
        post_list.append(reply_to)

    if main_post.replies.exists():#type:ignore
        for reply in main_post.replies.all():#type:ignore
            post_list.append(reply)

    post_list = make_post_objects(post_list, request.user)
    
    context = {
        'title': 'Post | Echo',
        'post_list': post_list
        }
    
    return render(request, 'posts/post_detail.html', context=context)