from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def signup_view(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))

    else:
        form = CustomUserCreationForm()
    
    context = {
        'title': 'Sign Up | Echo',
        'form': form
        }

    return render(request, 'users/signup.html', context=context)
        





