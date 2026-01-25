from django import forms
from .models import UnidadMedida, Categoria, Producto, ProductoImagen
from django.forms import inlineformset_factory 

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
        fields = ['nombre', 'slug']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Producto Profesional
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Excluimos slug y fechas porque son automáticos en el modelo
        exclude = ['slug', 'fecha_creacion', 'fecha_actualizacion'] 
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_oferta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Opcional'}), # Campo nuevo
            'tamano': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_tamano': forms.Select(attrs={'class': 'form-select'}),
            'grosor': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_grosor': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Creamos el conjunto de formularios para las imágenes
ProductoImagenFormSet = inlineformset_factory(
    Producto, 
    ProductoImagen, 
    fields=['imagen'], 
    extra=3,      # Número de espacios vacíos para nuevas imágenes
    can_delete=True # Permite borrar imágenes en la edición
)