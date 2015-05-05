from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control', "required":"", "autofocus":""}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control', "required":""}))
    rememberMe = forms.BooleanField(label="Remember me", required=False, initial=False)