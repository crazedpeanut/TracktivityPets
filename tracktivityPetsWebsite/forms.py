from django import forms

class LoginForm(Forms.form):
    email = forms.CharField(label="Email", max_length=100, widget=forms.EmailInput)
    password = form.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    rememberMe = forms.BooleanField(label="Remember me", widget=forms.CheckBoxInput)