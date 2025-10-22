import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Producto

@receiver(post_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)