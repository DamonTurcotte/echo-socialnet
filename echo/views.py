from django.shortcuts import render
from posts.models import Post
from users.models import EchoUser, Follow
from notifications.models import Alerts
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from oauth2_provider.decorators import protected_resource
import json


# Page logic is contained in Echo.JS and ajax_response(below)
def index(request):
    context = {
        'title': 'Home | Echo',
    }
    return render(request, 'echo/index.html', context=context)

@login_required
def follows_feed(request):
    context = {
        'title': 'My Follows | Echo',
    }
    return render(request, 'echo/index.html', context=context)


@ensure_csrf_cookie
def ajax_response(request):
    if request.method == 'GET':

        if request.GET['action'] == 'auth':
            if request.user.is_authenticated:
                return JsonResponse({
                    'status': 'user',
                    'user': request.user.username,
                    'uuid': request.user.uuid
                    })

            else:
                return JsonResponse({
                    'status': 'guest',
                    'user': None
                    })

        posts = Post.objects.order_by('timestamp').reverse().all()
        echouser = request.user
        post_list = list()
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        if page and limit:
            page = int(page)
            limit = int(limit)
            start = page * limit - limit
            end = page * limit

        total = 0

        data = {
            'post_list': post_list,
            'status': 'posts_retrieved',
            'total': total
        }

        if request.GET['action'] == 'get_feed_posts':
            posts = Post.objects.filter(reply_to=None, article_comment=None).annotate(
                popularity=(Count('likes') + Count('replies') + Count('reposts'))
                ).order_by('datestamp', 'popularity', 'timestamp').reverse()
            data['total'] = len(posts)
            posts = posts[start:end]

        if request.GET['action'] == 'get_follows_posts':
            follow_list = []
            follows = request.user.following.all()

            if not follows.exists():
                data['status'] = 'no_posts_retrieved'

            for follow in follows:
                follow_list.append(follow.follow)

            posts = Post.objects.filter(echouser__in=follow_list, reply_to=None).order_by('timestamp').reverse().all()
            data['total'] = len(posts)
            posts = posts[start:end]

        if request.GET['action'] == 'get_search_posts':
            query = request.GET['instance']
            posts = Post.objects.filter(post__icontains=query).annotate(
                popularity=(Count('likes') + Count('reposts') + Count('replies'))).order_by('popularity').reverse().all()
            
            data['total'] = len(posts)
            posts = posts[start:end]

        if request.GET['action'] == 'get_profile_replies':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = posts.exclude(reply_to=None)

            data['total'] = len(posts)
            posts = posts[start:end]

        if request.GET['action'] == 'get_profile_posts':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = posts.filter(reply_to=None)

            data['total'] = len(posts)
            posts = posts[start:end]

        if request.GET['action'] == 'get_profile_likes':
            echouser = EchoUser.objects.get(username=request.GET['instance'])
            posts = Post.objects.order_by('timestamp').reverse().filter(
                echouser=echouser.id).all()
            posts = echouser.liked.order_by('timestamp').reverse().all()  # type:ignore

            end = page * limit
            posts = posts[start:end]

        if request.GET['action'] == 'get_post_replies':
            post_uuid = request.GET['instance']
            posts = Post.objects.get(uuid=post_uuid)
            posts = posts.replies.all()  # type:ignore
            data['status'] = 'replies_retrieved'
            total = len(posts)

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
            post_view['num_reposts'] = post.num_reposts()
            post_view['object'] = ['post']

            alt_post_fields = [
                'reply_to_id',
                'reply_to_name',
                'repost_id',
                'repost_avatar',
                'repost_user',
                'repost_time',
                'repost_post',
                'article_title',
                'article_source',
                'article_category',
                'article_id',
                'article_image'
                ]
            
            for field in alt_post_fields:
                post_view[field] = ''

            try:
                post_view['reply_to_id'] = post.reply_to.uuid#type:ignore
                post_view['reply_to_name'] = post.reply_to.echouser.username#type:ignore
                post_view['object'] = 'reply'
            except:
                pass

            try:
                post_view['repost_id'] = post.repost_of.uuid#type:ignore
                post_view['repost_avatar'] = post.repost_of.echouser.avatar.url#type:ignore
                post_view['repost_user'] = post.repost_of.echouser.username#type:ignore
                post_view['repost_time'] = post.repost_of.when_posted()#type:ignore
                post_view['repost_post'] = post.repost_of.post#type:ignore
                post_view['object'] = 'repost'
            except:
                pass

            try:
                post_view['article_category'] = post.article_share.category#type:ignore
                post_view['article_id'] = post.article_share.uuid#type:ignore
                post_view['article_title'] = post.article_share.title#type:ignore
                post_view['article_source'] = post.article_share.source#type:ignore
                post_view['article_image'] = post.article_share.image#type:ignore
                post_view['object'] = 'share'
            except:
                pass

            if post.likes.filter(username=request.user).exists():
                post_view['liked'] = ' active'

            else:
                post_view['liked'] = ''

            post_list.append(post_view)

        return JsonResponse(data)

    if request.method == 'POST':

        if request.POST['action'] == 'like':
            post = Post.objects.get(uuid=request.POST['instance'])
            uuid = post.uuid
            
            if post.likes.filter(username=request.user).exists():
                post.likes.remove(request.user)
                data = {
                    'status': 'unliked',
                    'uuid': uuid
                }
                return JsonResponse(data)

            else:
                post.likes.add(request.user)
                
                if post.echouser.notifs.filter(type='like', by_user=request.user, post=post).exists() == False:
                    alert = Alerts(type='like', recipient=post.echouser, by_user=request.user, post=post)
                    alert.save()

                data = {
                    'status': 'liked',
                    'uuid': uuid
                }
                return JsonResponse(data)
            
        if request.POST['action'] == 'follow':
            if request.user.is_anonymous:
                return JsonResponse({'status': 'Anonymous users cannot follow'})

            profile = EchoUser.objects.get(uuid=request.POST['instance'])
            echouser = EchoUser.objects.get(uuid=request.user.uuid)
            data = {}

            if Follow.objects.filter(echouser=echouser, follow=profile).exists():
                Follow.objects.filter(echouser=echouser, follow=profile).delete()
                data['status'] = 'unfollowed'

            else:
                new_follow = Follow(echouser=echouser, follow=profile)
                new_follow.save()
                data['status'] = 'followed'

            return JsonResponse(data)

    return render(request, '404.html')


def search_response(request):
    query = request.GET.get('q')

    if request.GET['model'] == 'users':
        
        if query:
            user_list = []
            names = []
            results = EchoUser.objects.filter(username__startswith=query).exclude(username=request.user.username).order_by('last_login').reverse()
            for result in results:
                if len(user_list) < 5:
                    user = dict()
                    user['username'] = result.username
                    user['avatar'] = result.avatar.url
                    user_list.append(user)
                    names.append(result.username)
                
                else: break
            
            if len(user_list) < 5:
                results = EchoUser.objects.filter(username__icontains=query).exclude(username__in=names).exclude(username=request.user.username)
                for result in results:
                    if len(user_list) < 5:
                        user = dict()
                        user['username'] = result.username
                        user['avatar'] = result.avatar.url
                        user_list.append(user)

                    else: break
            
            if len(user_list) > 0:
                data = { 'users': user_list }
            else:
                data = { 'users': "no results" }

            return JsonResponse(data)

    return render(request, '404.html')

# simple placeholder page for future content
def under_construction(request):
    context = {'title': 'Under Construction | Echo Social'}
    return render(request, 'echo/todo.html', context=context)

def settings_view(request):
    context = {'title': 'Settings | Echo'}
    return render(request, 'echo/settings.html', context=context)



# oAuth2 response
@protected_resource(scopes=['read'])
def profile(request):
    return HttpResponse(json.dumps({
        'id': request.resource_owner.id,
        'uuid': request.resource_owner.uuid,
        'username': request.resource_owner.username,
        'avatar': request.resource_owner.avatar.url,
    }), content_type="application/json")