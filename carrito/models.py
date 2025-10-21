from django.db import models
# Importamos el modelo de usuario definido en settings.py
from django.conf import settings
from productos.models import Producto 

# La variable User apunta a tu CustomUser
User = settings.AUTH_USER_MODEL 

# ==================================
# 1. Modelo Carrito (ShoppingCart)
# ==================================

class Carrito(models.Model):
    """
    Representa el contenedor del carrito de compras. 
    Se vincula a un usuario autenticado o se gestiona por sesión para invitados.
    """
    # Si el usuario es nulo, el carrito se gestiona por ID en la sesión de Django.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carrito'
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        
    def __str__(self):
        return f"Carrito ID: {self.id}"

    def get_total_precio(self):
        """Calcula el precio total de todos los items en el carrito."""
        # Se asume que get_subtotal() existe en CarritoItem
        return sum(item.get_subtotal() for item in self.items.all())

# ==================================
# 2. Modelo Ítem de Carrito (CartItem)
# ==================================

class CarritoItem(models.Model):
    """
    Representa una joya y su cantidad dentro de un carrito específico.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', verbose_name="Contenedor de Carrito")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Joya")
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'carrito_item'
        verbose_name = "Ítem de Carrito"
        verbose_name_plural = "Ítems de Carrito"
        # Asegura que un producto solo aparezca una vez por carrito
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Carrito {self.carrito.id}"
        
    def get_subtotal(self):
        """Calcula el subtotal del ítem."""
        return self.producto.precio * self.cantidad