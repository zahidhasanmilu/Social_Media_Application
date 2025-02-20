
import re
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse
# from student.models import Student
# from student.forms import StudentForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView,DetailView

from django.contrib.auth.decorators import login_required
from app_user.utils import logout_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@logout_required
def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('username').strip()
        firstname = request.POST.get('first_name').strip()
        lastname = request.POST.get('last_name').strip() 
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()


        name = name.lower()
        email = email.lower()
        firstname = firstname.capitalize()
        lastname = lastname.capitalize()
        
        # Validate username
        if len(name) < 3 or len(name) > 15:
            messages.info(
                request, "Username must be between 3 and 15 characters.")
            print("Username must be between 3 and 15 characters.")
            return redirect('user_signup')

        # Check if username starts with a letter and contains only alphanumeric characters
        # Regex pattern:
        username_pattern = r'^[a-zA-Z][a-zA-Z0-9]*$'

        if not re.match(username_pattern, name):
            messages.info(
                request, "Username must start with a letter and contain only letters and numbers.")
            print(
                "Username must start with a letter and contain only letters and numbers.")
            return redirect('user_signup')

        # Password length validation (maximum 3 characters)
        if len(password) < 3:
            messages.info(
                request, "Password must be at least 3 characters long.")
            print("Password must be minimum at least 3 characters long")
            return redirect('user_signup')

        if password == confirm_password:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'User Already Exists')
                print('User already exists')
                return redirect('user_signup')

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exists")
                print('Email already exists')
                return redirect('user_signup')
            else:
                obj = User.objects.create_user(
                    first_name = firstname, last_name=lastname ,username=name, email=email, password=password)
                obj.set_password(password)
                obj.save()
                messages.success(request, 'User Create Succefully')
                return redirect('user_login')
        else:
            messages.info(request, "password doesn't match")
            return redirect('user_signup')
    return render(request, 'app_user/signup.html')


@logout_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        username = username.lower()
        password = password.lower()

        # Check if the username exists in the database
        if not User.objects.filter(username=username).exists():
            messages.warning(
                request, f'"{username}" - Username does not exist. make unique')
            return redirect('user_login')

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'{username} - Logged in successfully')
            return redirect('home')
        else:
            messages.warning(request, f'{username} Invalid credentials.')
            return redirect('user_login')
    return render(request, 'app_user/login.html')


@login_required
def user_logout(request):
    logout(request)
    # messages.success(request, 'Logged out successfully')
    return redirect('user_login')

'''
@login_required
def change_password(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, 'You must be logged in to change your password.')
        return redirect('login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        # Validate new password and confirmation
        if new_password != confirm_new_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        # Validate new password length (minimum 3 characters)
        if len(new_password) < 3:
            messages.error(
                request, 'Password must be at least 3 characters long.')
            return redirect('change_password')

        # Update password
        request.user.set_password(new_password)
        request.user.save()

        # Update session to prevent logout after password change
        update_session_auth_hash(request, request.user)

        messages.success(
            request, 'Your password has been updated successfully!')
        return redirect(reverse('profile', kwargs={'username': request.user.username}))

    return render(request, 'students/change_password.html')


    
class User_Profile(LoginRequiredMixin,ListView):
    model = Student
    template_name = "user_auth/profile.html"
    context_object_name = "students"  # Makes template code cleaner

    def get_queryset(self):
        """Retrieve all student profiles associated with the given username."""
        username = self.kwargs.get("username")
        self.profile_user = get_object_or_404(User, username=username)  # Store user object
        return Student.objects.filter(user=self.profile_user)

    def get_context_data(self, **kwargs):
        """Add the profile user to the context."""
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user  # Avoid duplicate queries
        return context
        
        '''