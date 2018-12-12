from django.shortcuts import render,redirect
from store.forms import *
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.core.files.storage import FileSystemStorage
import datetime

def index(request):
	carros = Carro.objects.all().order_by('-data_do_anuncio')
	return render(request,'store/index.html',{'carros':carros})

def cadastro(request):
	form = UserModelForm(request.POST)
	context = {'form':form}
	if request.method == 'POST':
		if request.POST['password_um'] != request.POST['password']:
			return render(request, 'store/cadastro.html', {'form':form, 'error_msg':'As senhas são diferentes!'})
		try:
			user = User.objects.get(email=request.POST['email'])
			return render(request, 'store/cadastro.html', {'form':form, 'error_msg':'Já existe uma pessoa com o email '+request.POST['email']})
		except User.DoesNotExist:
			if form.is_valid():
				form.save()
			return redirect('/login')
	else:
		form = UserModelForm()
		return render(request, 'store/cadastro.html', {'form':form})

def do_login(request):
	if request.method == 'POST':
		user = authenticate(username = request.POST['username'], password =  request.POST['password'])
		if user is not None:
			login(request,user)
			return redirect('/', user)
		return render(request, 'store/login.html',{'error_login':'Usuário ou senha inválidos'})
	return render(request, 'store/login.html')

def do_logout(request):
	logout(request)
	return redirect('/login')

@login_required(login_url='login')
def get_perfil(request):
	return render(request, 'store/perfil.html')

@login_required(login_url='login')
def add_car(request):
	if request.method == 'POST':
		#form = CarroModelForm(request.POST, request.FILES)
		up_image = request.FILES['foto']
		fs = FileSystemStorage()
		name = fs.save(up_image.name, up_image)
		url = fs.url(name)
		marca = Marca.objects.get(id=request.POST['marca'])
		carro = Carro(marca = marca, user = request.user, modelo = request.POST['modelo'], 
		ano_modelo = request.POST['ano_modelo'], ano_fabricacao = request.POST['ano_fabricacao'],
		numero_de_portas = request.POST['numero_de_portas'], foto = url, 
		descricao=request.POST['descricao'], preco=request.POST['preco'])
		carro.save()
		for acess in request.POST.getlist('acessorio'):
			acs = Acessorio.objects.get(id=acess)
			carro.acessorio.add(acs)
		return redirect('/add')
	else:
		form = CarroModelForm()
		return render(request, 'store/add_car.html', {'form':form})

def detalhes(request, carro_id):
	carro = Carro.objects.get(id=carro_id)
	sugestoes = Carro.objects.filter(descricao__contains=carro.modelo) | Carro.objects.filter(ano_fabricacao=carro.ano_fabricacao)
	return render(request, 'store/carro.html', {'carro':carro, 'sugestoes':sugestoes})

@login_required(login_url='login')
def editar(request, carro_id):
	carro = Carro.objects.get(id=carro_id)
	if request.method == 'POST':
		form = CarroModelForm(request.POST, instance=carro)
		if form.is_valid():
			form.save()
			return redirect('perfil')
		return render(request, 'store/update_car.html', {'form':form})
	else:
		form = CarroModelForm(instance=carro)
		return render(request, 'store/update_car.html', {'form':form})		
		
@login_required(login_url='login')
def apagar(request, carro_id):
	carro = Carro.objects.get(id=carro_id)
	carro.delete()
	return redirect('perfil')

@login_required(login_url='login')
def comprar(request, carro_id):
	carro = Carro.objects.get(id=carro_id)
	return render(request, 'store/compra.html', {'carro':carro})

def search(request):
	search = request.GET['search']
	carros = Carro.objects.filter(modelo__contains=search) | Carro.objects.filter(descricao__contains=search)
	sugestoes = Carro.objects.filter(ano_modelo__contains='20').order_by('data_do_anuncio')[:3]
	return render(request,'store/index.html',{'carros':carros,'sugestoes':sugestoes})

@login_required(login_url='login')
def venda(request, carro_id):
	carro = Carro.objects.get(id=carro_id)
	if request.method == 'POST':
		venda = Venda(carro=carro, comprador=request.user,
			prazo_pagamento=request.POST['prazo_pagamento'])
		venda.save()
		return redirect('comprar', carro_id)
	else:
		form = VendaModelForm()
		return render(request,'store/venda.html',{'form':form, 'carro':carro})