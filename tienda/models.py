from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('alimento', 'Alimento'),
        ('medicamento', 'Medicamento'),
        ('accesorio', 'Accesorio'),
        ('higiene', 'Productos de Higiene'),
        ('juguete', 'Juguetes'),
    ]

    TIPO_MASCOTA = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Reptil'),
        ('todos', 'Todos los tipos'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO, default='accesorio')
    tipo_mascota = models.CharField(max_length=20, choices=TIPO_MASCOTA, default='todos', verbose_name="Tipo de mascota")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    @property
    def en_oferta(self):
        return self.precio_descuento is not None and self.precio_descuento < self.precio

    @property
    def precio_final(self):
        return self.precio_descuento if self.en_oferta else self.precio

    @property
    def porcentaje_descuento(self):
        if self.en_oferta:
            return int(((self.precio - self.precio_descuento) / self.precio) * 100)
        return 0

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    @property
    def calificacion_promedio(self):
        comentarios = self.comentarios.filter(aprobado=True)
        if comentarios.exists():
            return round(sum(c.calificacion for c in comentarios) / comentarios.count(), 1)
        return 0

    @property
    def estrellas_lista(self):
        promedio = self.calificacion_promedio
        estrellas = []
        for i in range(5):
            if promedio > 0 and i < int(promedio):
                estrellas.append('full')
            elif promedio > 0 and i == int(promedio) and promedio % 1 >= 0.5:
                estrellas.append('half')
            else:
                estrellas.append('empty')
        return estrellas

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def cantidad_total(self):
        return sum(item.cantidad for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ['carrito', 'producto']

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio_final

class Orden(models.Model):
    ESTADO_ORDEN = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_proceso', 'En Proceso'),
        ('enviada', 'Enviada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    numero_orden = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN, default='pendiente')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.TextField()
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden #{self.numero_orden} - {self.usuario.username}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item de Orden'
        verbose_name_plural = 'Items de Orden'

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio
        super().save(*args, **kwargs)

class Comentario(models.Model):
    CALIFICACION_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    calificacion = models.IntegerField(choices=CALIFICACION_CHOICES)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=True)  # Para moderación futura

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-fecha_creacion']
        unique_together = ['producto', 'usuario']  # Un comentario por usuario por producto

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.producto.nombre}"

    @property
    def estrellas_display(self):
        return '★' * self.calificacion + '☆' * (5 - self.calificacion)