from django.shortcuts import render



def alerts_view(request):

    context = {
        'title': 'Alerts | Echo'
    }
    
    return render(request, 'notifications/alerts.html', context=context)