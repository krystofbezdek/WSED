from django.views import generic
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class HomeView(generic.ListView):
    template_name = 'WSED/home.html'
    context_object_name = 'nothing'

    def get_queryset(self):
        return []

class FinishView(generic.ListView):
    template_name = 'WSED/finish.html'
    context_object_name = 'nothing'

    def get_queryset(self):
        return []


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Authenticate and login the user
            login(request, new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
