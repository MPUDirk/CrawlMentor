from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from auth.forms import AuthenticationForm, RegistrationForm


# Create your views here.
class LoginView(BaseLoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('auth:login')

class SignupView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
