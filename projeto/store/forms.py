# -*- coding: utf-8 -*-
from django.forms import ModelForm 
from django import forms 
from django.contrib.auth.models import User
from store.models import *

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength':255}),
            'email':forms.TextInput(attrs={'class':'form-control', 'maxlength':255}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'maxlength':255}),

        }

        error_messages={
            'username':{
                'required':'Campo obrigatório'
            },
            'email':{
                'required':'Campo obrigatório'
            },
            'password':{
                'required':'Campo obrigatório'
            },
        }
    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user  


class CarroModelForm(forms.ModelForm):
    class Meta:
        model = Carro
        #fields = ['marca','modelo', 'ano_modelo', 'ano_fabricacao', 'nume_portas','foto']
        exclude = ['user']
        widgets={
        	'marca':forms.Select(attrs={'class':'form-control'}),
            'modelo':forms.TextInput(attrs={'class':'form-control', 'maxlength':255}),
            'ano_modelo':forms.TextInput(attrs={'class':'form-control', 'maxlength':255}),
            'ano_fabricacao':forms.TextInput(attrs={'class':'form-control', 'maxlength':255}),
            'nume_portas':forms.NumberInput(attrs={'class':'form-control'}),
            'descricao':forms.Textarea(attrs={'class':'form-control'}),
            'foto':forms.FileInput(attrs={'class':'form-control'}),
            'preco':forms.NumberInput(attrs={'class':'form-control'}),
            'acessorio':forms.CheckboxSelectMultiple(attrs={'class':'checkbox form-control'}),
        }
        error_messages = {
	        'modelo':{
	        	'required':'Informe o modelo do veiculo!'
	        },
	        'ano_fabricacao':{
	        	'required':'Informe o ano de fabricação do veiculo!'
	        }
        }

class AcessorioModelForm(forms.ModelForm):
    class Meta:
        model = Acessorio
        fields = ['nome']
        widgets={
             'nome':forms.TextInput(attrs={'class':'form-control', 'maxlength':255})
        }

class VendaModelForm(forms.ModelForm):
	class Meta:
		model = Venda
		fields = ['prazo_pagamento']
		widgets ={
			'prazo_pagamento':forms.DateInput(attrs={'class':'form-control', 'type':'date'})
		}

		error_messages = {
	        'prazo_pagamento':{
	        	'required':'Informe o prazo desejado!'
	        },
        }