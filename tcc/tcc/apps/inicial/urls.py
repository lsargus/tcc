from django.urls import path

from . import views
from .forms import loginForm
from .view import cadastroView

urlpatterns = [
    path('', views.index, name='index'),
    path('projeto', views.projeto, name='projeto'),
    path('login/', loginForm.login, name='login'),
    path('logout/', loginForm.logout, name='logout'),
    path('cadastroUser/', cadastroView.cadastro_novo_usuario, name='cadastroUser'),
]
