from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
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


@login_required
def profile_view(request, uuid):
    profile = EchoUser.objects.get(uuid=uuid)

    context = {
        'title': f'{profile.username} | Echo',
        'profile': {
            'username': profile.username,
            'bio': profile.bio,
            'avatar': profile.avatar,
            'email': profile.email,
            'date_joined': profile.date_joined.date(),
            'last_login': profile.since_last_login()
        },
    }

    return render(request, 'users/profile.html', context=context)
