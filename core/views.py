from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages
from productos.models import UnidadMedida, Categoria, Producto
from productos.forms import UnidadMedidaForm

# Vistas principales
def inicio(request):
    return render(request, 'core/inicio.html')

def menu(request):
    return render(request, 'core/menu.html')

#  *************************************************************
#         MANEJO DE UNIDADES DE MEDIDA PARA PRODUCTOS
#   SE USA EL SISTEMA DE MESAJE DE DJANGO PARA NOTIFICACIONES 
#  *************************************************************
def unidadesNew(request):
    if request.method == "POST":
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Unidad creada exitosamente.")
                return redirect('unidadesshow')
            except Exception as e:
                messages.error(request, f"Error al guardar la unidad: {e}")
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
    else:
        form = UnidadMedidaForm()
    
    return render(request, 'productos/unidadesNew.html', {
        'form': form
    })

def unidadesShow(request):
    unidades = UnidadMedida.objects.all()
    return render(request, 'productos/unidadesShow.html', {
        'unidades': unidades
    })

def unidadesEdit(request, id):
    unidad = get_object_or_404(UnidadMedida, pk=id)
    form = UnidadMedidaForm(instance=unidad)
    return render(request, 'productos/unidadesEdit.html', {
        'form': form,
        'unidades': unidad
    })

def unidadesUpdate(request, id):
    unidad = get_object_or_404(UnidadMedida, pk=id)
    if request.method == "POST":
        form = UnidadMedidaForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Unidad actualizada correctamente.")
            return redirect('unidadesshow')
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
            return render(request, 'productos/unidadesEdit.html', {
                'form': form,
                'unidades': unidad
            })
    else:
        form = UnidadMedidaForm(instance=unidad)

    return render(request, 'productos/unidadesEdit.html', {
        'form': form,
        'unidades': unidad
    })

def unidadesDestroy(request, id):
    unidad = get_object_or_404(UnidadMedida, pk=id)
    try:
        unidad.delete()
        messages.success(request, "Unidad eliminada correctamente.")
    except IntegrityError:
        messages.warning(request, "No se puede eliminar la unidad porque está referenciada por otros registros.")
    return redirect('unidadesshow')