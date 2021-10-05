from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


class CadastroForm(forms.Form):
    first_name = forms.CharField(max_length=150, label='Nome')
    last_name = forms.CharField(max_length=150, label='Sobrenome')
    username = forms.CharField(max_length=150, label='Nome de usuário', required=True)
    email = forms.CharField(max_length=250, required=True, label='E-mail')
    senha = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label='Senha')

    def clean_email(self):
        email = self.cleaned_data['email']

        validate_email(email)

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if len(senha) < 8:
            raise ValidationError('Senha deve possuir mais de 8 caractéres!')

        # verifica se a senha possui caracteres numericos, letras minusculas, letras maiusculas e caracteres especiais
        if re.search(r'[0-9]', senha) is None or \
                re.search(r'[a-z]', senha) is None or \
                re.search(r'[A-Z]', senha) is None or \
                re.search(r'[!@#$%<^&*?]', senha) is None:
            raise ValidationError(
                'Senha deve possuir caracteres numéricos, letras maiúsculas, letras minúsculas e caracteres especiais !')
