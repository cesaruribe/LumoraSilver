from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Modelo de Usuario Personalizado (CustomUser)
class CustomUser(AbstractUser):
    """Extiende el modelo User por defecto de Django.
    Campos principales del modelo 
    Estos son los campos más comunes que incluye:
    •   username: nombre de usuario único
    • 	password: contraseña (almacenada como hash)
    • 	email: dirección de correo electrónico
    • 	 first_name y last_name : nombres del usuario
    • 	is_active : indica si el usuario está activo
    • 	is_staff : indica si puede acceder al admin
    • 	is_superuser: indica si tiene todos los permisos
    • 	last_login: fecha del último acceso
    • 	date_joined : fecha de creación del usuario """
    
    # Campo adicional para e-commerce
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    
    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

# 2. Modelo de Ubicación Geográfica
class Departamento(models.Model):
    codigo_departamento = models.IntegerField(primary_key=True)
    nombre_departamento = models.CharField(max_length=56)

    class Meta:
        db_table = "departamento"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre_departamento


class Municipio(models.Model):
    codigo_municipio = models.IntegerField(primary_key=True)
    nombre_municipio = models.CharField(max_length=27)
    tipo_municipio_isla_area_no_municipalizada = models.CharField(max_length=22)
    longitud = models.CharField(max_length=10)
    latitud = models.CharField(max_length=9)

    # Relación con Departamento
    codigo_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        db_column="codigo_departamento",
        related_name="municipios"
    )

    class Meta:
        db_table = "municipio"
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return f"{self.nombre_municipio} ({self.codigo_departamento.nombre_departamento})"

# 3. Modelo de Direcciones (para envío y facturación)
class Direccion(models.Model):
    """Almacena las diferentes direcciones de un usuario."""
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='direcciones', verbose_name="Usuario")
    etiqueta = models.CharField(max_length=50, help_text="Ej: Casa, Oficina, Dirección de Regalo")
    calle_numero = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=50, default="Colombia") # O el país de venta
    es_predeterminada = models.BooleanField(default=False)

    class Meta:
        db_table = 'direccion'
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return f"{self.etiqueta}: {self.calle_numero}, {self.ciudad}"