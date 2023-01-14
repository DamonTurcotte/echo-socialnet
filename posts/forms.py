from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'post': forms.Textarea(attrs={
                'class': 'create-post-text',
                'placeholder': 'Write your post here...',
                'autocomplete': 'off',
                'autofocus': True
                })
        }