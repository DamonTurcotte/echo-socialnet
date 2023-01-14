from django.shortcuts import render
from posts.models import Post
from users.models import EchoUser
from django.http import JsonResponse


def index(request):
    posts = Post.objects.order_by('timestamp').reverse().all()
    if request.method == 'POST':
        post = Post.objects.get(uuid=request.POST['post'])
        uuid = post.uuid

        if request.POST['action'] == 'like':
            if post.likes.filter(username=request.user).exists():
                post.likes.remove(EchoUser.objects.get(username=request.user))
                print('Unliked')
                data = {
                    'status': 'unliked',
                    'uuid': uuid
                }
                return JsonResponse(data)

            else:
                post.likes.add(EchoUser.objects.get(username=request.user))
                data = {
                    'status': 'liked',
                    'uuid': uuid
                }
                return JsonResponse(data)

    post_list = list()
    for post in posts:
        post_view = dict()
        post_view['post'] = post
        if post.likes.filter(username=request.user).exists():
            post_view['liked'] = ' active'
        else:
            post_view['liked'] = ''
        post_list.append(post_view)

    context = {
        'title': 'Home | Echo Social',
        'post_list': post_list
    }
    return render(request, 'echo/index.html', context=context)
