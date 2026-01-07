from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, DireccionForm
from .models import Direccion, Municipio, Departamento 
from django.http import JsonResponse

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) # Login automático tras registro
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            # Redirigir a 'next' si existe (útil si venía del carrito) o a inicio
            next_url = request.GET.get('next', 'inicio')
            return redirect(next_url)
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

@login_required
def perfil(request):
    # Obtenemos las direcciones del usuario para mostrarlas en el perfil
    direcciones = request.user.direcciones.all()
    return render(request, 'cuentas/perfil.html', {
        'usuario': request.user,
        'direcciones': direcciones
    })

@login_required
def eliminar_cuenta(request):
    if request.method == "POST":
        user = request.user
        # Anonimización para GDPR/Leyes de datos
        user.username = f"deleted_{user.id}_{user.username[:3]}" # Preserva unicidad
        user.email = ""
        user.first_name = ""
        user.last_name = ""
        user.is_active = False # Desactivar, no borrar
        user.save()
        
        logout(request) # <--- IMPORTANTE: Cerrar sesión
        messages.info(request, "Tu cuenta ha sido eliminada correctamente.")
        return redirect('inicio')
    
    return render(request, 'cuentas/eliminar_cuenta.html')

@login_required
def agregar_direccion(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user
            
            # Mapeamos los objetos seleccionados a los campos de texto del modelo
            departamento = form.cleaned_data['departamento']
            municipio = form.cleaned_data['municipio']
            
            direccion.estado_provincia = departamento.nombre_departamento
            direccion.ciudad = municipio.nombre_municipio
            
            # Si esta es la primera dirección, establecer como predeterminada
            if not request.user.direcciones.exists():
                direccion.es_predeterminada = True
            
            direccion.save()
            messages.success(request, 'Dirección guardada exitosamente.')
            return redirect('cuentas:perfil')
        else:
            # Si el formulario no es válido, mostrar errores
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            print(form.errors)  # Para debug
    else:
        form = DireccionForm()
    
    return render(request, 'cuentas/agregar_direccion.html', {'form': form})

# Función para la carga dinámica vía AJAX
def ajax_cargar_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    municipios = Municipio.objects.filter(codigo_departamento_id=departamento_id).order_by('nombre_municipio')
    return JsonResponse(list(municipios.values('codigo_municipio', 'nombre_municipio')), safe=False)