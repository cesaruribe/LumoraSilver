from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from productos.models import UnidadMedida, Categoria, Producto
from productos.forms import UnidadMedidaForm, CategoriaForm, ProductoForm
from django.db import IntegrityError

# Vistas para Productos
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
                return redirect('productos:unidadesshow')
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
            return redirect('productos:unidadesshow')
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
    return redirect('productos:unidadesshow')

#  *************************************************************
#         MANEJO DE CATEGORIAS DE LOS PRODUCTOS
#   SE USA EL SISTEMA DE MESAJE DE DJANGO PARA NOTIFICACIONES 
#  *************************************************************
def categoriasNew(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Categoria creada exitosamente.")
                return redirect('productos:categoriasshow')
            except Exception as e:
                messages.error(request, f"Error al guardar la Categoria: {e}")
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
    else:
        form = CategoriaForm()
    
    return render(request, 'productos/categoriasNew.html', {
        'form': form
    })

def categoriasShow(request):
    categoria = Categoria.objects.all()
    return render(request, 'productos/categoriasShow.html', {
        'categorias': categoria
    })

def categoriasEdit(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(instance=categoria)
    return render(request, 'productos/categoriasEdit.html', {
        'form': form,
        'categorias': categoria
    })

def categoriasUpdate(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "categoria actualizada correctamente.")
            return redirect('productos:categoriasshow')
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
            return render(request, 'productos/categoriasEdit.html', {
                'form': form,
                'categorias': categoria
            })
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'productos/categoriasEdit.html', {
        'form': form,
        'categorias': categoria
    })

def categoriasDestroy(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    try:
        categoria.delete()
        messages.success(request, "Categoria eliminada correctamente.")
    except IntegrityError:
        messages.warning(request, "No se puede eliminar la categoria porque está referenciada por otros registros.")
    return redirect('productos:categoriasshow')
#  *************************************************************
#         MANEJO DE PRODUCTOS
#   SE USA EL SISTEMA DE MESAJE DE DJANGO PARA NOTIFICACIONES 
#  *************************************************************
def productosNew(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Producto creado exitosamente.")
                return redirect('productos:productosshow')
            except Exception as e:
                messages.error(request, f"Error al guardar el Producto: {e}")
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
    else:
        form = ProductoForm()
    
    return render(request, 'productos/productosNew.html', {
        'form': form
    })

def productosShow(request):
    producto = Producto.objects.all()
    return render(request, 'productos/productosShow.html', {
        'productos': producto
    })

def productosEdit(request, id):
    producto = get_object_or_404(Producto, pk=id)
    form = ProductoForm(instance=producto)
    return render(request, 'productos/productosEdit.html', {
        'form': form,
        'productos': producto
    })

def productosUpdate(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos:productosshow')
        else:
            messages.warning(request, "Por favor corrige los errores del formulario.")
            return render(request, 'productos/productosEdit.html', {
                'form': form,
                'producto': producto
            })
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/productosEdit.html', {
        'form': form,
        'producto': producto
    })

def productosDestroy(request, id):
    producto = get_object_or_404(Producto, pk=id)
    try:
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
    except IntegrityError:
        messages.warning(request, "No se puede eliminar el Producto porque está referenciada por otros registros.")
    return redirect('productos:productosshow')