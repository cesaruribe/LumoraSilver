from django.db import models
from django.conf import settings
from productos.models import Producto

class Carrito(models.Model):
    # Relación uno a uno con el usuario
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='carrito',
        null=True, blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username if self.usuario else 'Anónimo'}"

    @property
    def total_pagar(self):
        """Calcula el gran total sumando todos los items."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def cantidad_total(self):
        """Cuenta el total de joyas en el carrito."""
        return sum(item.cantidad for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        """Multiplica la cantidad por el precio final del producto."""
        return self.producto.precio_final * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"