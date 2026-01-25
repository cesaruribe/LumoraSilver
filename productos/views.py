from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from productos.models import UnidadMedida, Categoria, Producto
from productos.forms import UnidadMedidaForm, CategoriaForm, ProductoForm, ProductoImagenFormSet
from django.db import IntegrityError
from django.db.models import Q 
from django.core.paginator import Paginator 
# Importamos el decorador para restringir el acceso
from django.contrib.auth.decorators import login_required


# Vistas para Productos
#  *************************************************************
#         MANEJO DE UNIDADES DE MEDIDA PARA PRODUCTOS
#  *************************************************************

@login_required
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
    
    return render(request, 'productos/unidadesNew.html', {'form': form})

@login_required
def unidadesShow(request):
    unidades = UnidadMedida.objects.all()
    return render(request, 'productos/unidadesShow.html', {'unidades': unidades})

@login_required
def unidadesEdit(request, id):
    unidad = get_object_or_404(UnidadMedida, id=id)
    form = UnidadMedidaForm(instance=unidad)
    return render(request, 'productos/unidadesEdit.html', {'form': form, 'unidad': unidad})

@login_required
def unidadesUpdate(request, id):
    unidad = get_object_or_404(UnidadMedida, id=id)
    form = UnidadMedidaForm(request.POST, instance=unidad)
    if form.is_valid():
        form.save()
        messages.success(request, "Unidad actualizada correctamente.")
        return redirect('productos:unidadesshow')
    return render(request, 'productos/unidadesEdit.html', {'form': form, 'unidad': unidad})

@login_required
def unidadesDestroy(request, id):
    unidad = get_object_or_404(UnidadMedida, id=id)
    try:
        unidad.delete()
        messages.success(request, "Unidad eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la unidad porque está siendo usada por productos.")
    return redirect('productos:unidadesshow')


#  *************************************************************
#         MANEJO DE CATEGORIAS
#  *************************************************************

@login_required
def categoriasNew(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada.")
            return redirect('productos:categoriasshow')
    else:
        form = CategoriaForm()
    return render(request, 'productos/categoriasNew.html', {'form': form})

@login_required
def categoriasShow(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/categoriasShow.html', {'categorias': categorias})

@login_required
def categoriasEdit(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(instance=categoria)
    return render(request, 'productos/categoriasEdit.html', {'form': form, 'categoria': categoria})

@login_required
def categoriasUpdate(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, "Categoría actualizada.")
        return redirect('productos:categoriasshow')
    return render(request, 'productos/categoriasEdit.html', {'form': form, 'categoria': categoria})

@login_required
def categoriasDestroy(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    try:
        categoria.delete()
        messages.success(request, "Categoría eliminada.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la categoría porque tiene productos asociados.")
    return redirect('productos:categoriasshow')


#  *************************************************************
#         MANEJO DE PRODUCTOS (ADMINISTRACIÓN)
#  *************************************************************

@login_required
def productosNew(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        formset = ProductoImagenFormSet(request.POST, request.FILES) # Captura el set de imágenes
        
        if form.is_valid() and formset.is_valid():
            producto = form.save()
            # Guardamos el formset asociándolo al producto recién creado
            imagenes = formset.save(commit=False)
            for img in imagenes:
                img.producto = producto
                img.save()
            
            messages.success(request, "Producto y galería creados con éxito.")
            return redirect('productos:productosshow')
    else:
        form = ProductoForm()
        formset = ProductoImagenFormSet()
    
    return render(request, 'productos/productosNew.html', {
        'form': form,
        'formset': formset
    })

@login_required
def productosShow(request):
    # 1. Obtener todos los productos base
    productos_list = Producto.objects.all().order_by('-fecha_creacion')
    categorias = Categoria.objects.all()

    # 2. Capturar parámetros del formulario GET
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    oferta = request.GET.get('oferta')

    # 3. Aplicar filtros si existen
    if query:
        productos_list = productos_list.filter(
            Q(nombre__icontains=query) | Q(codigo__icontains=query)
        )
    
    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)

    if oferta == 'si':
        productos_list = productos_list.filter(precio_oferta__isnull=False)
    elif oferta == 'no':
        productos_list = productos_list.filter(precio_oferta__isnull=True)

    # 4. Configurar Paginación (ejemplo: 10 productos por página)
    paginator = Paginator(productos_list, 10)
    page = request.GET.get('page')
    productos = paginator.get_page(page)

    # 5. Pasar todo al contexto
    return render(request, 'productos/productosShow.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
        'oferta': oferta
    })


@login_required
def productosEdit(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        formset = ProductoImagenFormSet(request.POST, request.FILES, instance=producto)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos:productosshow')
    else:
        form = ProductoForm(instance=producto)
        formset = ProductoImagenFormSet(instance=producto)
    
    return render(request, 'productos/productosEdit.html', {
        'form': form, 
        'formset': formset, 
        'producto': producto
    })

@login_required
def productosUpdate(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ProductoForm(request.POST, request.FILES, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado.")
        return redirect('productos:productosshow')
    return render(request, 'productos/productosEdit.html', {'form': form, 'producto': producto})

@login_required
def productosDestroy(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect('productos:productosshow')


#  *************************************************************
#         VISTAS PÚBLICAS (CATÁLOGO Y DETALLE)
#  *************************************************************

def catalogo(request):
    # Optimizamos la consulta
    productos = Producto.objects.select_related('categoria').filter(activo=True).order_by('-fecha_creacion')
    categorias = Categoria.objects.all()

    # Captura de filtros desde el GET
    query = request.GET.get('q')
    min_p = request.GET.get('min_p')
    max_p = request.GET.get('max_p')
    categoria_slug = request.GET.get('categoria')

    if query:
        productos = productos.filter(nombre__icontains=query)
    
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)

    if min_p:
        productos = productos.filter(precio__gte=min_p)
        
    if max_p:
        productos = productos.filter(precio__lte=max_p)

    return render(request, 'productos/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'min_p': min_p,
        'max_p': max_p
    })

def productoDetalle(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)
    
    # Calculamos el porcentaje de ahorro
    ahorro_porcentaje = 0
    if producto.precio_oferta and producto.precio > 0:
        descuento = producto.precio - producto.precio_oferta
        ahorro_porcentaje = (descuento / producto.precio) * 100

    return render(request, 'productos/productoDetalle.html', {
        'producto': producto,
        'ahorro_porcentaje': ahorro_porcentaje
    })