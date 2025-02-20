from django.contrib import admin
from .models import Post,UserProfile
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_content', 'post_image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'post_content')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display= ('bio','works_at', 'studies_at','dob')
    list_filter = ('dob',)
    
    