from django.db import models

# ***************************************************************        
# Tabla de Unidades de Medida para tamaño y grosor
# P.E : Gramos, Kilogramos, Onzas, Centimetros, Milimetros etc.
# ***************************************************************
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

# *************************************************        
# Tabla de Categorias a Ofrecer en el sitio web
# P.E : Anillos, Cadenas, Aretes, etc.
# *************************************************
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    # Opcional: para categorías jerárquicas
    # categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

# *************************************************        
# Tabla de Productos a Ofrecer en el sitio web
# *************************************************
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)   
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Tamaño y grosor como opcionales (no todos los productos los necesitan)
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
    
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        # Para evitar productos duplicados
        unique_together = ['nombre', 'categoria', 'codigo']
