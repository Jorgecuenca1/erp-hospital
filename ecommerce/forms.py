from django import forms
from .models import CategoriaProducto, Producto, Cliente, Carrito, LineaCarrito, Pedido, LineaPedido, Pago

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = '__all__'

class LineaCarritoForm(forms.ModelForm):
    class Meta:
        model = LineaCarrito
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class LineaPedidoForm(forms.ModelForm):
    class Meta:
        model = LineaPedido
        fields = '__all__'

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__' 