from django.db import models
from django.conf import settings
from productos.models import Producto 
from cuentas.models import Direccion # Importamos la dirección definida en la app 'cuentas'

# Accede a tu modelo de usuario personalizado (CustomUser)
User = settings.AUTH_USER_MODEL 

# ==================================
# Modelos de Pedido (Orden de Compra) 📦
# ==================================

class Pedido(models.Model):
    """Representa un pedido finalizado y pagado."""
    
    # Opciones de estado del pedido
    ESTADOS = (
        ('PEN', 'Pendiente de Pago'),
        ('PAG', 'Pagado'),
        ('PRO', 'En Proceso'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    )

    # Vínculo con el cliente que hizo la orden
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='pedidos',
        verbose_name="Cliente"
    )
    
    # Dirección de Envío (vinculada a la dirección guardada del usuario)
    direccion_envio = models.ForeignKey(
        Direccion, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Dirección de Envío"
    )
    
    # Datos de la transacción y totales
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Subtotal")
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo de Envío")
    total_final = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Pagado")
    
    # Estado del pedido
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN', verbose_name="Estado")
    
    # Identificador de la transacción de la pasarela de pago (esencial)
    id_transaccion = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text="ID proporcionado por la pasarela de pago (ej. Stripe, PayPal)"
    )

    class Meta:
        db_table = 'pedido'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"

    def calcular_total_final(self):
        """Calcula y actualiza el total final (neto + envío)."""
        self.total_final = self.total_neto + self.costo_envio
        self.save()

# ==================================
# 3. Modelo Ítem de Pedido (OrderItem)
# ==================================

class PedidoItem(models.Model):
    """
    Almacena los detalles de cada producto dentro de un pedido. 
    Asegura la inmutabilidad de la información de la joya al momento de la compra.
    """
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Pedido"
    )
    
    # Vínculo al producto. Se acepta NULL por si el producto se elimina del catálogo.
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Joya (Ref. Catálogo)"
    ) 
    
    # Datos CLAVE copiados para inmutabilidad:
    nombre_producto = models.CharField(max_length=200, verbose_name="Nombre al Comprar")
    precio_al_momento = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio Unitario de Compra",
        help_text="Precio al que se compró la joya, sin importar cambios futuros."
    ) 
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")

    class Meta:
        db_table = 'pedido_item'
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto} en Pedido {self.pedido.id}"
        
    def get_subtotal(self):
        """Calcula el subtotal del ítem en la orden."""
        return self.precio_al_momento * self.cantidad