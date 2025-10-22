import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Producto

@receiver(post_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)

@receiver(pre_save, sender=Producto)
def eliminar_imagen_anterior_si_se_reemplaza(sender, instance, **kwargs):
    if not instance.pk:
        return  # Producto nuevo, no hay imagen anterior

    try:
        producto_anterior = Producto.objects.get(pk=instance.pk)
    except Producto.DoesNotExist:
        return

    imagen_anterior = producto_anterior.imagen
    imagen_nueva = instance.imagen

    # Si se limpió la imagen o se reemplazó
    if imagen_anterior and imagen_anterior != imagen_nueva:
        if os.path.isfile(imagen_anterior.path):
            os.remove(imagen_anterior.path)