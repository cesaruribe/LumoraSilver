from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Elimina usuarios que no han activado su cuenta después de 3 días'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Definimos el límite de tiempo (3 días atrás desde ahora)
        limite = timezone.now() - timedelta(days=3)
        
        # Filtramos: usuarios NO activos CREADOS antes del límite
        usuarios_por_borrar = User.objects.filter(
            is_active=False, 
            date_joined__lt=limite
        )
        
        cantidad = usuarios_por_borrar.count()
        
        if cantidad > 0:
            usuarios_por_borrar.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Se han eliminado {cantidad} usuarios inactivos con éxito.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No se encontraron usuarios inactivos para eliminar.')
            )