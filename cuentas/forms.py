from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Direccion
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'placeholder': field.label
            })


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ['usuario']

    def __init__(self, *args, **kwargs):
        super(DireccionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'placeholder': field.label
            })

class PerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono']

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'placeholder': field.label
            })


from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm'
                # No usar 'placeholder' con form-floating
            })