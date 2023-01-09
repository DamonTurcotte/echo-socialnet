from django.shortcuts import render


def index(request):
    try:
        uuid = request.user.uuid
    except: uuid = None

    context = {
        'title': 'Home | Echo Social',
        'uuid': uuid
    }
    return render(request, 'echo/index.html', context=context)