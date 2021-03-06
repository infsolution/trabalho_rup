from django.shortcuts import render,redirect
from store.forms import *
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.core.files.storage import FileSystemStorage
import datetime

def index(request):
	imoveis = Imovel.objects.all().order_by('-data_do_anuncio')[:3]
	return render(request,'store/index.html',{'imoveis':imoveis})

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
	mensagens = []
	imoveis = Imovel.objects.filter(user=request.user)
	for im in imoveis:
		try:
			mens = Mensagem.objects.filter(imovel=im)
			for m in mens:
				mensagens.append(m)
		except Exception:
			print('Exception')			
	return render(request, 'store/perfil.html',{'mensagens':mensagens})

@login_required(login_url='login')
def add_imovel(request):
	ok_msg = 'Ocorreu um erro ao criar o anúncio!'
	if request.method == 'POST':
		tipo = Tipo.objects.get(id=request.POST['tipo'])
		status = Status.objects.get(id=request.POST['status'])
		imovel = Imovel(user= request.user, area = request.POST['area'], 
			numero_de_quarto = request.POST['numero_de_quarto'], 
			numero_de_banheiros = request.POST['numero_de_banheiros'],
			numero_de_vagas  = request.POST['numero_de_vagas'], 
			descricao = request.POST['descricao'], 
			preco = request.POST['preco'], 
			preco_condominio = request.POST['preco_condominio'], 
			status = status, tipo=tipo)
		imovel.save()
		address = Endereco(imovel=imovel, logradouro = request.POST['logradouro'], 
			nome_logradouro = request.POST['nome_log'], numero = request.POST['numero'], 
			bairro = request.POST['bairro'], cidade = request.POST['cidade'], estado = request.POST['estado'])
		address.save()
		for image in request.FILES.getlist('images'):
			up_image = image
			fs = FileSystemStorage()
			name = fs.save(up_image.name, up_image)
			url = fs.url(name)
			foto = Foto(imovel = imovel, image = url)
			foto.save()
		ok_msg = 'O imovel foi anunciado'
		return redirect('/add', {'ok_msg':ok_msg})
	else:
		form = ImovelModelForm()
		sugestoes = Imovel.objects.filter(preco__lte=360000)
		return render(request, 'store/add_imovel.html', {'form':form, 'sugestoes':sugestoes})

def detalhes(request, imovel_id):
	imovel = Imovel.objects.get(id=imovel_id)
	sugestoes = Imovel.objects.filter(preco__lte=imovel.preco)
	return render(request, 'store/imovel.html', {'imovel':imovel, 'sugestoes':sugestoes})

@login_required(login_url='login')
def editar(request, imovel_id):
	imovel = Imovel.objects.get(id=imovel_id)
	if request.method == 'POST':
		form = ImovelModelForm(request.POST, instance=imovel)
		if form.is_valid():
			form.save()
			return redirect('perfil')
		return render(request, 'store/update_car.html', {'form':form})
	else:
		form = ImovelModelForm(instance=imovel)
		return render(request, 'store/update_imovel.html', {'form':form})		
		
@login_required(login_url='login')
def apagar(request, imovel_id):
	imovel = Imovel.objects.get(id=imovel_id)
	imovel.delete()
	return redirect('perfil')


def search(request):
	search = request.GET['search']
	sugestoes = []
	imoveis = Imovel.objects.filter(descricao__contains=search)
	if len(imoveis) <= 0:
		sugestoes = Imovel.objects.filter(preco__lte=360000).order_by('data_do_anuncio')[:3]
	return render(request,'store/search.html',{'imoveis':imoveis,'sugestoes':sugestoes})


@login_required(login_url='login')
def venda(request, imovel_id):
	imovel = Imovel.objects.get(id=imovel_id)
	if request.method == 'POST':
		mensagem = Mensagem(imovel=imovel, interessado = request.user, mensagem = request.POST['mensagem'])
		mensagem.save()
		return redirect('index')
	else:
		form = MensagemModelForm()
		return render(request,'store/mensagem.html',{'form':form, 'imovel':imovel})