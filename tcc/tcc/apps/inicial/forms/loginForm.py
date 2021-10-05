from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            auth_login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'login.html', {'nome_pag': 'Login', 'msg': 'usuário inválido'})

    return render(request, 'login.html', {'nome_pag': 'Login', 'msg': ''})


def logout(request):
    auth_logout(request)
    return redirect('index')
