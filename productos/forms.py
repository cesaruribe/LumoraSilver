from django import forms
from .models import UnidadMedida, Categoria, Producto

# Formulario para Unidad de Medida
class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre', 'simbolo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','slug']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['fecha_creacion', 'fecha_actualizacion']  # Campos automáticos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tamano': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_tamano': forms.Select(attrs={'class': 'form-select'}),
            'grosor': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_grosor': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }