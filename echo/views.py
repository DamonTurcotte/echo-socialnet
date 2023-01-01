from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home | Echo Social'
    }
    return render(request, 'echo/index.html', context=context)