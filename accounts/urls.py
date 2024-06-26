from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)