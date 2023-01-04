from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import EchoUserCreationForm
from .models import EchoUser
from django.contrib.auth.decorators import login_required

def signup_view(request):

    if request.method == 'POST':
        form = EchoUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))

    else:
        form = EchoUserCreationForm()
    
    context = {
        'title': 'Sign Up | Echo',
        'form': form
        }

    return render(request, 'users/signup.html', context=context)


def profile_view(request, uuid):
    data = EchoUser.objects.get(uuid=uuid)
    context = {
        'title': f'{data.username} | Echo',
        'profile': {
            'username': data.username,
            'bio': data.bio,
            'avatar': data.avatar
        }
    }

    return render(request, 'users/profile.html', context=context)
