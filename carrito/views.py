from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import Carrito, ItemCarrito
from django.contrib import messages

@login_required
def agregarAlCarrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # 1. Validar si el producto tiene stock disponible de entrada
    if producto.stock <= 0:
        messages.error(request, f"Lo sentimos, {producto.nombre} se acaba de agotar.")
        return redirect('productos:catalogo')

    # 2. Capturar cantidad solicitada
    try:
        cantidad_solicitada = int(request.POST.get('cantidad', 1))
        if cantidad_solicitada < 1:
            cantidad_solicitada = 1
    except ValueError:
        cantidad_solicitada = 1

    # 3. Obtener o crear el carrito
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # 4. Obtener el item si ya existe para calcular la cantidad proyectada
    item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    cantidad_actual_en_carrito = 0 if item_created else item.cantidad
    cantidad_final_proyectada = cantidad_actual_en_carrito + cantidad_solicitada

    # 5. VALIDACIÓN CRÍTICA: ¿La suma supera el stock real?
    if cantidad_final_proyectada > producto.stock:
        # Si ya no puede agregar más, restauramos la cantidad anterior si el item no era nuevo
        if item_created:
            item.delete() # No permitimos crear el item si no hay stock suficiente
        
        messages.error(request, 
            f"No puedes agregar {cantidad_solicitada} unidad(es). "
            f"Solo quedan {producto.stock} en total y ya tienes {cantidad_actual_en_carrito} en tu bolsa."
        )
        return redirect('productos:productodetalle', id=producto.id)

    # 6. Si pasa todas las validaciones, guardamos
    item.cantidad = cantidad_final_proyectada
    item.save()
    
    messages.success(request, f"¡Añadido! Ahora tienes {item.cantidad} unidad(es) de {producto.nombre} en tu bolsa.")
    return redirect('carrito:vercarrito')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from django.contrib import messages

@login_required
def verCarrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # UX Preventivo: Validamos si el stock cambió mientras el usuario tenía la bolsa abierta
    for item in carrito.items.all():
        if item.producto.stock < item.cantidad:
            if item.producto.stock == 0:
                item.delete()
                messages.warning(request, f"El producto {item.producto.nombre} se agotó y fue removido de tu bolsa.")
            else:
                item.cantidad = item.producto.stock
                item.save()
                messages.info(request, f"La cantidad de {item.producto.nombre} se ajustó al stock disponible.")
                
    return render(request, 'carrito/verCarrito.html', {'carrito': carrito})

@login_required
def actualizarCantidad(request, item_id, accion):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    
    if accion == 'sumar':
        if item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save()
        else:
            messages.error(request, "No hay más unidades disponibles de esta joya.")
    elif accion == 'restar':
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
            messages.info(request, "Producto eliminado de la bolsa.")
            
    return redirect('carrito:vercarrito')

@login_required
def eliminarDelCarrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    nombre = item.producto.nombre
    item.delete()
    messages.warning(request, f"{nombre} eliminado de la bolsa.")
    return redirect('carrito:vercarrito')