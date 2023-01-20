from django.shortcuts import render
from posts.models import Post
from users.models import EchoUser
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    posts = Post.objects.order_by('timestamp').filter(reply_to=None).reverse().all()

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


@ensure_csrf_cookie
def ajax_response(request):
    if request.method == 'GET':
        print(request.GET)

        if request.GET['action'] == 'auth':
            if request.user.is_authenticated:
                return JsonResponse({'status': 'user'})

            else:
                return JsonResponse({'status': 'guest'})

        posts = Post.objects.all()
        echouser = request.user
        post_list = list()

        # RETURN PROFILE TAB POSTS

        if request.GET['action'] == 'get_profile_replies':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = posts.exclude(reply_to=None)

        if request.GET['action'] == 'get_profile_posts':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = posts.filter(reply_to=None)

        if request.GET['action'] == 'get_profile_likes':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = echouser.liked.order_by('timestamp').reverse().all()  # type:ignore

        data = {
            'post_list': post_list,
            'status': 'posts_retrieved'
        }

        if request.GET['action'] == 'get_post_replies':
            post_uuid = request.GET['instance']
            posts = Post.objects.get(uuid=post_uuid)
            posts = posts.replies.all()  # type:ignore
            data['status'] = 'replies_retrieved'

        for post in posts:
            post_view = dict()
            post_view['echouser'] = post.echouser.username
            post_view['echouser_id'] = post.echouser.uuid
            post_view['avatar'] = post.echouser.avatar.url
            post_view['post_id'] = post.uuid
            post_view['post'] = post.post
            post_view['when_posted'] = post.when_posted()
            post_view['num_likes'] = post.num_likes()
            post_view['num_replies'] = post.num_replies()

            try:
                post_view['reply_to_id'] = post.reply_to.uuid#type:ignore
                post_view['reply_to_name'] = post.reply_to.echouser.username#type:ignore
            except:
                post_view['reply_to_id'] = ''
                post_view['reply_to_name'] = ''

            if post.likes.filter(username=request.user).exists():
                post_view['liked'] = ' active'

            else:
                post_view['liked'] = ''

            post_list.append(post_view)

        return JsonResponse(data)

    if request.method == 'POST':
        post = Post.objects.get(uuid=request.POST['instance'])
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

    return render(request, '404.html')
