
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from .forms import activate_user
from django.views.generic import TemplateView

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("mailconfirm")
    template_name = "registration/signup.html"
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
    
class ActivateView(TemplateView):
    template_name = "registration/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        return super().get(request, result=result, **kwargs)
    

    



