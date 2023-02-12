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
    main_post = Post.objects.get(uuid=uuid)
    post_author = main_post.echouser.username

    try:
        if request.GET['action'] == 'get_post_detail':
            post_as_list = [main_post]
            post_list = make_post_objects(post_as_list, request.user)

            data = {
                'post_list': post_list,
                'status': 'post_retrieved'
                }

            return JsonResponse(data)

    except:
        context = {
         'title': f'{post_author}\'s Post | Echo'
        }

        return render(request, 'posts/post_detail.html', context=context)
    
    return render(request, 'posts/post_detail.html')
