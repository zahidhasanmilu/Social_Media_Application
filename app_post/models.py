from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date
from PIL import Image
import os

# To automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(blank=True, null=True)
    post_image = models.ImageField(
        upload_to="posts/image/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.post_content[:50]}...'

    @staticmethod
    def all_posts():
        return Post.objects.all()




class UserProfile(models.Model):

    MARITAL_STATUS = (
        ('single', 'single'),
        ('married', 'married'),
        ('divorced', 'divorced'),
        ('widowed', 'widowed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', default='default_profile_picture.jpeg', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    works_at = models.TextField(blank=True, null=True)
    studies_at = models.TextField(blank=True, null=True)
    lives_in = models.TextField(blank=True, null=True)
    marital_status = models.CharField(
        max_length=50, choices=MARITAL_STATUS, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Resize the profile picture before saving
        if self.profile_picture:
            img = Image.open(self.profile_picture)
            img = img.resize((540, 540), Image.Resampling.LANCZOS)   # Resize image to 540x540
            img.save(self.profile_picture.path)  # Save the resized image

        super().save(*args, **kwargs)  # Call the original save method


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # This ensures it only runs when a new User is created
        UserProfile.objects.create(user=instance)

# Signal to save UserProfile when the User instance is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()  #