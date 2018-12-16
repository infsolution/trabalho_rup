from django.db import models
from django.contrib.auth.models import User



class Tipo(models.Model):
	nome_tipo = models.CharField(max_length=50)
	def __str__(self):
		return self.nome_tipo
class Status(models.Model):
	nome_status = models.CharField(max_length=50)
	def __str__(self):
		return self.nome_status

class Imovel(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='meus_imoveis')
	area = models.IntegerField(default=0)
	numero_de_quarto = models.IntegerField(default=2)
	numero_de_banheiros = models.IntegerField(default=2)
	numero_de_vagas = models.IntegerField(default=2)
	descricao = models.TextField(null=True, blank=True)
	preco = models.FloatField(default=0)
	preco_condominio = models.FloatField(default=0)
	data_do_anuncio = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	tipo = models.ForeignKey(Tipo,on_delete = models.CASCADE, related_name='tipo')
	status = models.ForeignKey(Status,on_delete = models.CASCADE, related_name='status')
	def __str__(self):
		return str(self.id)

class Venda(models.Model):
	imovel = models.OneToOneField(Imovel, on_delete = models.CASCADE,related_name='venda')
	comprador = models.ForeignKey(User,on_delete = models.CASCADE, related_name='comprador')
	concluida = models.BooleanField(default=False)
	data_venda = models.DateField(auto_now_add=True)
	prazo_pagamento = models.DateField(null=True, blank=True)
	pagamento_ok = models.BooleanField(default=False)

class Foto(models.Model):
	imovel = models.ForeignKey(Imovel,on_delete=models.CASCADE,related_name='fotos')
	image=models.ImageField(blank=True, null=True,upload_to = 'media/')


class Endereco(models.Model):
 	imovel = models.OneToOneField(Imovel, on_delete = models.CASCADE,related_name='endereco')
 	logradouro = models.CharField(max_length=20)
 	nome_logradouro = models.CharField(max_length=255)
 	numero = models.IntegerField(default=0)
 	bairro = models.CharField(max_length=255)
 	cidade = models.CharField(max_length=255)
 	estado = models.CharField(max_length=255)

class Caracteristica(models.Model):
 	imovel = models.ForeignKey(Imovel,on_delete=models.CASCADE,related_name='caracteristicas')
 	nome_caracteristica = models.CharField(max_length=255)

class Mensagem(models.Model):
	imovel = models.ForeignKey(Imovel,on_delete=models.CASCADE,related_name='mensagens')
	interessado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interessado')
	mensagem = models.TextField()
	data_mensagem = models.DateTimeField(auto_now_add=True, null=True, blank=True)