from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import LoginForm



from django.contrib import messages
from django.utils.translation import gettext_lazy as _ #para la traduccion



# viastas del index 
class HomeView(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determine if the current user has any products with zero stock
        if self.request.user.is_authenticated:
            from products.models import Products
            context['has_alerts'] = Products.objects.filter(product=self.request.user, stock=0).exists()
        else:
            context['has_alerts'] = False
        return context
    
# vistas de Login
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, ('Bienvenido, {}!').format(user.username))    
                return HttpResponseRedirect(reverse('home'))
                
            else:
                messages.add_message(request, messages.ERROR, _('Nombre de usuario o contraseña incorrectos.'))
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


#vista de logout
@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, _('Se ha cerrado sesión correctamente.'))
    return HttpResponseRedirect(reverse('home'))



  





