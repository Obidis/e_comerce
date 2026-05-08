from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.views.generic import FormView

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _ #para la traduccion
from django.utils import translation
from django.views import View




# viastas del index 
class HomeView(TemplateView):
    template_name = "general/home.html"

   
    

# vistas de Login
class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

   

#vista de logout
@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, _('Se ha cerrado sesión correctamente.'))
    return HttpResponseRedirect(reverse('home'))


# vista de registro 
class RegisterView(CreateView):
    template_name = "general/register.html"
   

  
# Vista para mostrar y gestionar las recetas favoritas de un usuario




