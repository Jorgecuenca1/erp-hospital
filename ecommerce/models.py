from django.db import models
from django.conf import settings

# Create your models here.

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=16, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.usuario)

class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Carrito {self.id} - {self.cliente}"

class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=16, decimal_places=2)
    estado = models.CharField(max_length=30, choices=[('PENDIENTE','Pendiente'),('PAGADO','Pagado'),('ENVIADO','Enviado'),('ENTREGADO','Entregado'),('CANCELADO','Cancelado')], default='PENDIENTE')
    direccion_envio = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    metodo = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Pago {self.id} - {self.pedido}"
