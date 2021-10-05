from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from tcc.apps.inicial.forms.cadastroForm import CadastroForm


def cadastro_novo_usuario(request):
    if request.method == 'POST':

        form = CadastroForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(request.POST["username"], email=request.POST["email"],
                                            password=request.POST["senha"])
            user.last_name = request.POST["last_name"]
            user.save()
            #realiza o login
            auth_login(request, user)

            return redirect('index')
        else:
            return render(request, "cadastro.html", {'nome_pag': 'Cadastro', 'form': form})

    else:
        form = CadastroForm()

        return render(request, "cadastro.html", {'nome_pag': 'Cadastro', 'form': form, 'msg': ''})

