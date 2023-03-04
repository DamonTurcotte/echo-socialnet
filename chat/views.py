from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Chat
from users.models import EchoUser
from .forms import CreatePvtMessageForm
from chat.utils import message_list



@login_required
def chat_view(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        recipient = EchoUser.objects.get(username=recipient)

        if Chat.objects.filter(users=recipient).filter(users=request.user).exists():
            chat_instance = Chat.objects.filter(users=request.user).filter(users=recipient)[0]
            chat_uuid = chat_instance.uuid

        else:
            Chat.objects.create().users.set([request.user, recipient])
            chat_instance = Chat.objects.filter(users=request.user).filter(users=recipient)[0]
            chat_uuid = chat_instance.uuid

        return JsonResponse({'chat_uuid':chat_uuid})

    chat_querylist = Chat.objects.filter(users=request.user).distinct().order_by('timestamp').reverse()
    chats = []
    
    for chat_obj in chat_querylist:

        chat = {}

        for user in chat_obj.users.all():
            if user == request.user:
                pass
            else:
                chat['user'] = user

        chat['uuid'] = chat_obj.uuid
        chat['last_user'] = chat_obj.last_user
        chat['last_message'] = chat_obj.last_message
        chat['timestamp'] = chat_obj.when_last()

        chats.append(chat)

    context = {
        'title': 'Private Messages | Echo',
        'chats': chats
    }

    return render(request, 'chat/list.html', context=context)

@login_required
@ensure_csrf_cookie
def message_view(request, uuid):
    chat = Chat.objects.get(uuid=uuid)
    user = request.user
    recipient = chat.users.exclude(username=request.user.username)[0]

    messages = message_list(chat, user)

    context = {
        'title': 'Private Messages | Echo',
        'user': user,
        'recipient': recipient,
        'chat': chat,
        'messages': messages
    }

    return render(request, 'chat/message.html', context=context)

def chat_response(request):
    if request.method == 'POST':
        if request.POST['action'] == 'post_message':
            sender = EchoUser.objects.get(username=request.POST['sender'])
            receiver = EchoUser.objects.get(username=request.POST['receiver'])
            message = request.POST['message']
            chat = Chat.objects.get(uuid=request.POST['chat'])

            form = CreatePvtMessageForm(data={
                'chat': chat,
                'sender': sender,
                'receiver': receiver,
                'message': message,
            })

            if form.is_valid():
                form.save()
                messages = message_list(chat, request.user)

                return JsonResponse({'messages':messages})
            
            else:
                return JsonResponse({})

    return render(request, '404.html')