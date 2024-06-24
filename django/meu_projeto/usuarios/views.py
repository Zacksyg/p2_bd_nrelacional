from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_inicial')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)
            return redirect('pagina_inicial')
        else:
            return HttpResponse('Email ou senha inválidos')
        

def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')
