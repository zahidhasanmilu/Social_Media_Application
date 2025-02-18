from django import forms
from .models import Post
import os

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content', 'post_image']
    
    def clean_post_image(self):
        image = self.cleaned_data.get('post_image')

        if image:
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if ext not in valid_extensions:
                raise forms.ValidationError("image extention type should be only- 'jpg, jpeg, png'")
        
        return image
