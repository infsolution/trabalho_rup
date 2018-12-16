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


class ImovelModelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        exclude = ['user']
        widgets={
            'area':forms.NumberInput(attrs={'class':'form-control'}),
        	'numero_de_quarto':forms.NumberInput(attrs={'class':'form-control'}),
            'numero_de_banheiros':forms.NumberInput(attrs={'class':'form-control'}),
            'numero_de_vagas':forms.NumberInput(attrs={'class':'form-control'}),
            'descricao':forms.Textarea(attrs={'class':'form-control'}),
            'preco':forms.NumberInput(attrs={'class':'form-control'}),
            'preco_condominio':forms.NumberInput(attrs={'class':'form-control'}),
            'tipo':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
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
class MensagemModelForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['mensagem']
        widgets = {
            'mensagem':forms.Textarea(attrs={'class':'form-control'})
        }

