from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Direccion

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono', 'password1', 'password2']


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ['usuario']