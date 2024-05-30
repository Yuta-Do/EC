from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginFrom
from django.http import HttpResponseRedirect

from django.contrib.auth import logout
from django.shortcuts import redirect
from cart.models import Cart

class IndexView(TemplateView):
    template_name = "index.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('product_list')) 
        return super().dispatch(request, *args, **kwargs)

    
class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request,account_id=account_id, password=password)
        login(self.request, user)
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('product_list'))  
        return super().dispatch(request, *args, **kwargs)

# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('product_list'))
        
        # ログインユーザーのカートが存在しない場合は新しいカートを作成
        if request.user.is_authenticated and not hasattr(request.user, 'cart'):
            Cart.objects.create(user=request.user)
        
        return super().dispatch(request, *args, **kwargs)

def LogoutView(request):
    logout(request)
    return redirect('accounts:index')