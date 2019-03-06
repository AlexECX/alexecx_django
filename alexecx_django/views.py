from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import SignUpForm

class SignupView(LoginView):
    """Enregistrement d'un nouvelle utilisateur

    Si la fonction reçois un formulaire d'inscription valide, enregistre
    le nouvelle utilisateur dans la bd, le connecte, et le retourne à la
    page d'acceuil.
    Sinon, lui renvoie la page d'inscription.
    """
    form_class = SignUpForm
    template_name = 'alexecx_django/signup_page.html'
    success_url = reverse_lazy('alexecx_django:index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request, 
            username=username, 
            password=raw_password
        )
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
