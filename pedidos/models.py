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
    ESTADOS = [
        ('PEN', 'Pendiente de Pago'),
        ('PAG', 'Pagado'),
        ('PRO', 'En Proceso'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    # Vínculo con el cliente que hizo la orden
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='pedidos',
        verbose_name="Cliente"
    )
    
    # Dirección de Envío (vinculada a la dirección guardada del usuario)
    # Se agrega related_name para permitir la validación de inmutabilidad en 'cuentas'
    direccion_envio = models.ForeignKey(
        Direccion, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='pedidos_realizados',
        verbose_name="Dirección de Envío"
    )

    # Identificación única del pedido para seguimiento
    referencia = models.CharField(max_length=50, unique=True, verbose_name="Referencia de Pedido")
    
    # Totales monetarios
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    costo_envio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Fechas de control
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pedido")
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Estado actual
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN', verbose_name="Estado")

    # Campo para comentarios adicionales del cliente o administrador
    notas = models.TextField(blank=True, null=True, verbose_name="Notas del Pedido")

    class Meta:
        db_table = 'pedido'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pedido {self.referencia} - {self.usuario.get_full_name() if self.usuario else 'Anónimo'}"


# ==================================
# Detalles del Pedido (Líneas) 💍
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
    # Si el precio del producto cambia mañana, el pedido mantiene el precio original
    nombre_producto = models.CharField(max_length=200, verbose_name="Nombre al Comprar")
    precio_al_momento = models.DecimalField(
        max_digits=12, 
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
        return f"{self.cantidad} x {self.nombre_producto}"

    @property
    def get_subtotal(self):
        return self.precio_al_momento * self.cantidad