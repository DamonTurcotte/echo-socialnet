from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home | Echo Social',
        'uuid': request.user.uuid
    }
    return render(request, 'echo/index.html', context=context)