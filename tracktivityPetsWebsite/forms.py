from django import forms
from django.forms.widgets import Widget

class LoginForm(forms.Form):
    email = forms.CharField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control', 'id':'loginEmail', "required":"", "autofocus":""}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control', 'id':'loginPassword', "required":""}))
    rememberMe = forms.BooleanField(label="Remember me", required=False, initial=False)
    
class RegisterForm(forms.Form):
    firstname = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'First name', 'class':'form-control', 'id':'regFirstName', 'required':'', 'autofocus':''}))
    surname = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Surname', 'class':'form-control', 'id': 'regSurname', 'required':''}))
    email = forms.CharField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control', 'id':'regEmail', "required":""}))
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control', 'id':'regUsername', "required":""}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control', 'id':'regPassword', "required":"", "autofocus":""}))
    confirmPass = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Confirm password', 'class':'form-control', 'id':'regConfirmPass' ,"required":"", "autofocus":""}))