from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm 
from django.http import HttpResponseRedirect   
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')   
                      
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, ('Usuario creado correctamente.'))
            return HttpResponseRedirect(reverse ('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})











@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, _('Se ha cerrado sesión correctamente.'))
    return HttpResponseRedirect(reverse('home'))




