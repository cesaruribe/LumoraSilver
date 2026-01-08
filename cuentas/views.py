from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, DireccionForm, EditarPerfilForm 
from .models import Direccion, Municipio, Departamento 
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# --- FUNCIÓN AUXILIAR DE ENVÍO ---
def enviar_email_activacion(request, usuario):
    """
    Función para generar y enviar el correo de activación.
    Evita repetir código en la vista de registro.
    """
    dominio = get_current_site(request).domain
    subject = 'Activa tu cuenta de E-commerce'
    mensaje = render_to_string('cuentas/email_confirmacion.html', {
        'usuario': usuario,
        'dominio': dominio,
        'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
        'token': default_token_generator.make_token(usuario),
    })
    
    email = EmailMessage(subject, mensaje, to=[usuario.email])
    email.content_subtype = "html" 
    email.send()

# --- VISTAS ---

def registro(request):
    User = get_user_model()
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        email_post = request.POST.get('email')
        
        # 1. LÓGICA DE REENVÍO: Si el usuario ya existe pero NO está activo
        usuario_existente = User.objects.filter(email=email_post, is_active=False).first()
        
        if usuario_existente:
            enviar_email_activacion(request, usuario_existente)
            messages.info(request, 'Ya tenías un registro pendiente. Hemos reenviado el enlace de activación a tu correo.')
            return redirect('cuentas:login')

        # 2. REGISTRO NUEVO: Si el formulario es válido
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False 
            usuario.save()

            enviar_email_activacion(request, usuario)

            messages.info(request, 'Te hemos enviado un correo. Por favor, confirma tu cuenta para poder iniciar sesión.')
            return redirect('cuentas:login')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

def activar_cuenta(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.is_active = True 
        usuario.save()
        login(request, usuario) 
        messages.success(request, '¡Cuenta activada con éxito! Bienvenido.')
        return redirect('inicio')
    else:
        return render(request, 'cuentas/activacion_fallida.html')


@login_required
def perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado correctamente!')
            return redirect('cuentas:perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    direcciones = request.user.direcciones.all()
    return render(request, 'cuentas/perfil.html', {
        'form': form,
        'direcciones': direcciones,
        'usuario': request.user # Esto nos permite acceder a last_login
    })

@login_required
def eliminar_cuenta(request):
    if request.method == "POST":
        user = request.user
        user.username = f"deleted_{user.id}_{user.username[:3]}" 
        user.email = ""
        user.first_name = ""
        user.last_name = ""
        user.is_active = False 
        user.save()
        
        logout(request) 
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
            
            departamento = form.cleaned_data['departamento']
            municipio = form.cleaned_data['municipio']
            
            direccion.estado_provincia = departamento.nombre_departamento
            direccion.ciudad = municipio.nombre_municipio
            
            if not request.user.direcciones.exists():
                direccion.es_predeterminada = True
            
            direccion.save()
            messages.success(request, 'Dirección guardada exitosamente.')
            return redirect('cuentas:perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = DireccionForm()
    
    return render(request, 'cuentas/agregar_direccion.html', {'form': form})

@login_required
def editar_direccion(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
    
    if direccion.tiene_pedidos:
        messages.warning(request, "Esta dirección no se puede editar por historial de pedidos.")
        return redirect('cuentas:perfil')

    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            dir_editada = form.save(commit=False)
            
            # Lógica de seguridad: Si solo tiene esta dirección, debe ser predeterminada
            total_direcciones = request.user.direcciones.count()
            if total_direcciones <= 1:
                dir_editada.es_predeterminada = True
            
            # Guardamos (el método save() del modelo se encarga de desactivar las otras)
            dir_editada.save()
            
            messages.success(request, "Dirección actualizada correctamente.")
            return redirect('cuentas:perfil')
    else:
        form = DireccionForm(instance=direccion)
    
    return render(request, 'cuentas/agregar_direccion.html', {
        'form': form, 
        'editando': True
    })

@login_required
def eliminar_direccion(request, pk):
    if request.method == "POST":
        direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
        
        if direccion.tiene_pedidos:
            messages.error(request, "No es posible eliminar direcciones vinculadas a compras realizadas.")
        else:
            direccion.delete()
            messages.success(request, "Dirección eliminada correctamente.")
    return redirect('cuentas:perfil')

@login_required
def marcar_predeterminada(request, pk):
    # Obtenemos la dirección asegurando que sea del usuario logueado
    direccion = get_object_or_404(Direccion, pk=pk, usuario=request.user)
    
    direccion.es_predeterminada = True
    direccion.save() # Esto dispara la lógica de "unicidad" que creamos en el modelo
    
    messages.success(request, f'"{direccion.etiqueta}" es ahora tu dirección predeterminada.')
    return redirect('cuentas:perfil')
            
def ajax_cargar_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    municipios = Municipio.objects.filter(codigo_departamento_id=departamento_id).order_by('nombre_municipio')
    return JsonResponse(list(municipios.values('codigo_municipio', 'nombre_municipio')), safe=False)