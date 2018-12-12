from django.db import models
from django.contrib.auth.models import User


class Marca(models.Model):
	nome = models.CharField(max_length=100)
	sigle = models.CharField(max_length=3)
	def __str__(self):
		return self.nome

class Acessorio(models.Model):
	nome = models.CharField(max_length=256)
	def __str__(self):
		return self.nome

class Carro(models.Model):
	marca = models.ForeignKey(Marca, on_delete = models.CASCADE, related_name='carros')
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='meus_carros')
	modelo = models.CharField(max_length=100)
	ano_modelo = models.CharField(max_length=4)
	ano_fabricacao = models.CharField(max_length=4)
	numero_de_portas = models.IntegerField(default=2)
	descricao = models.TextField(null=True, blank=True)
	preco = models.FloatField(default=0)
	data_do_anuncio = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	foto = models.ImageField(null=True, blank=True, upload_to = 'media/')
	acessorio = models.ManyToManyField(Acessorio,blank=True)
	def __str__(self):
		return self.modelo

class Venda(models.Model):
	carro = models.OneToOneField(Carro, on_delete = models.CASCADE,related_name='venda')
	comprador = models.ForeignKey(User,on_delete = models.CASCADE, related_name='comprador')
	concluida = models.BooleanField(default=False)
	data_venda = models.DateField(auto_now_add=True)
	prazo_pagamento = models.DateField(null=True, blank=True)
	pagamento_ok = models.BooleanField(default=False)