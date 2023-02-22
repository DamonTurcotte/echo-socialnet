from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from .forms import EchoUserCreationForm
from .models import EchoUser, Follow
from django.contrib.auth.decorators import login_required
from PIL import Image
import math
from io import BytesIO

def signup_view(request):

    if request.method == 'POST':
        form = EchoUserCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            hashed_pass = make_password(request.POST['password'])

            try:
                request.FILES['avatar']
                upload = True
            except:
                upload = False

            if upload == True:
                x = int(math.floor(float(request.POST['x'])))
                y = int(math.floor(float(request.POST['y'])))
                width = int(math.floor(float(request.POST['width'])))
                height = int(math.floor(float(request.POST['height'])))
                dimensions = int(math.floor(float(request.POST['dimensions'])))

                image = Image.open(request.FILES['avatar'])
                resized_image = image.resize((width, height), Image.ANTIALIAS)
                new_image = resized_image.crop((x, y, dimensions+x, dimensions+y))

                new_image_io = BytesIO()
                new_image.save(new_image_io, format='webp')

                user = form.save(commit=False)

                user.password = hashed_pass

                user.avatar.delete(save=False)
                temp_name = f'{user.uuid}.webp'
                user.avatar.save(
                    temp_name,
                    content=ContentFile(new_image_io.getvalue()),
                    save=False
                )
                user.save()
                login(request, user)
                return redirect(reverse('home'))
            
            else:
                user = form.save(commit=False)
                user.password = hashed_pass
                user.save()
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
    follow_status = ''

    if profile == request.user:
        follow_status = 'self'

    elif Follow.objects.filter(echouser=request.user, follow=profile).exists():
        follow_status = 'unfollow'

    else:
        follow_status = 'follow'

    context = {
        'title': f'{profile.username} | Echo',
        'profile': {
            'username': profile.username,
            'bio': profile.bio,
            'avatar': profile.avatar,
            'email': profile.email,
            'date_joined': profile.date_joined.date(),
            'last_login': profile.since_last_login(),
            'num_following': profile.num_following(),
            'num_followers': profile.num_followers(),
            'follow_status': follow_status
        },
    }

    return render(request, 'users/profile.html', context=context)
