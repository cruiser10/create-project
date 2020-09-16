from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from .forms import ProjectForm
from .models import Project
from django.views import View

class RegisterView(View):
    def get(self,request):
        return render(request, 'accounts/register.html', {'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            return redirect(reverse('login'))

        return render(request, 'accounts/register.html', {'form': form }) 

class LoginView(View):
    def get(self,request):
        return render(request, 'accounts/login.html', {'form': AuthenticationForm() })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is None:
                return render(
                    request,
                    'accounts/login.html',
                    {'form':form, 'invalid_cred':True}

                )
            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(request,'accounts/login.html', {'form':form, 'invalid_cred':True} )

            login(request, user)

            return redirect(reverse('profile'))     


class ProfileView(LoginRequiredMixin, View):
    def get(self,request):
        projects = Project.objects.filter(created_by=request.user).all()
        return render(request,'accounts/profile.html', {'form':ProjectForm(), 'projects':projects })

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()    
        return render(request, 'accounts/profile.html', {'form':form} )    