from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class SignUpForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'form-control'}) )

    class Meta:
        model = User
        fields = ( 'name', 'address','tel', 'country','username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                name=self.cleaned_data['name'],
                address=self.cleaned_data['address'],
                tel=self.cleaned_data['tel'],
                country=self.cleaned_data['country'],
                user=user,
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))