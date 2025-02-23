from django import forms
from .models import Post,UserProfile
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
    
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'bio', 'works_at', 'studies_at', 'lives_in', 'marital_status', 'dob']

        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write something about yourself'}),
            'works_at': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'studies_at': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution name'}),
            'lives_in': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current city'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """ Populate form fields with existing user data """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        """ Save both User and UserProfile models """
        user_profile = super().save(commit=False)
        user = user_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            user_profile.save()
        return user_profile
