from django.urls import path
from . import views as user_view
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='tmpl_accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tmpl_accounts/logout.html'), name='logout'),
    path('register/', user_view.register, name='register'),
    path('dashboard/', user_view.CriandoContato.as_view(),
         name='dashboard')
]
