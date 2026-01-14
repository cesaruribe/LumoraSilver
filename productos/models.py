from django.db import models
from django.utils.text import slugify

# Tabla de Unidades de Medida para tamaño y grosor
class UnidadMedida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.simbolo})"

    class Meta:
        db_table = 'unidad_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

# Tabla de Categorías
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True) # URLs amigables

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

# Tabla de Productos
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)   
    nombre = models.CharField(max_length=40)
    slug = models.SlugField(max_length=250, unique=True, blank=True) # SEO
    descripcion = models.TextField()
    
    # Precios y Ofertas
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Medidas (opcionales)
    tamano = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    unidad_tamano = models.ForeignKey(
        UnidadMedida, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='productos_tamano'
    )
    
    grosor = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    unidad_grosor = models.ForeignKey(
        UnidadMedida, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='productos_grosor'
    )
    
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def precio_final(self):
        """Retorna el precio de oferta si existe, de lo contrario el normal."""
        return self.precio_oferta if self.precio_oferta else self.precio

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        unique_together = ['nombre', 'categoria', 'codigo']