from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Direccion, Departamento, Municipio 

# --- FORMULARIO DE REGISTRO ---
class RegistroForm(UserCreationForm):
    """
    Formulario para el registro de nuevos clientes.
    Optimizado para capturar el teléfono necesario para e-commerce.
    """
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )
    first_name = forms.CharField(required=True, label="Nombres")
    last_name = forms.CharField(required=True, label="Apellidos")
    telefono = forms.CharField(
        required=True, 
        label="Teléfono Móvil",
        help_text="Necesario para coordinar la entrega de tus pedidos."
    )

    class Meta:
        model = CustomUser # Vinculado a tu modelo CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos clases de Bootstrap a todos los campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# --- FORMULARIO DE DIRECCIÓN ---
class DireccionForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento",
        empty_label="Seleccione un Departamento",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'select_departamento'})
    )
    
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Municipio / Ciudad",
        empty_label="Seleccione primero un departamento",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'select_municipio'})
    )

    class Meta:
        model = Direccion
        fields = ['etiqueta', 'calle_numero', 'departamento', 'municipio', 'codigo_postal', 'es_predeterminada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # MEJORA UX: Clase form-control a todos para que se expandan correctamente
        for name, field in self.fields.items():
            if name not in ['departamento', 'municipio', 'es_predeterminada']:
                field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Ingrese {field.label.lower()}'})