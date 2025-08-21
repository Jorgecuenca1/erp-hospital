from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import CategoriaProducto, Producto, Cliente, Carrito, LineaCarrito, Pedido, LineaPedido, Pago
from .forms import CategoriaProductoForm, ProductoForm, ClienteForm, CarritoForm, LineaCarritoForm, PedidoForm, LineaPedidoForm, PagoForm


class EcommerceDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de ecommerce"""
    template_name = 'ecommerce/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ecommerce'
        context['productos_total'] = 0  # Placeholder
        return context

# Create your views here.

# CategoriaProducto
class CategoriaProductoListView(ListView):
    model = CategoriaProducto
class CategoriaProductoDetailView(DetailView):
    model = CategoriaProducto
class CategoriaProductoCreateView(CreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    success_url = reverse_lazy('ecommerce:categoriaproducto_list')
class CategoriaProductoUpdateView(UpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    success_url = reverse_lazy('ecommerce:categoriaproducto_list')
class CategoriaProductoDeleteView(DeleteView):
    model = CategoriaProducto
    success_url = reverse_lazy('ecommerce:categoriaproducto_list')

# Producto
class ProductoListView(ListView):
    model = Producto
class ProductoDetailView(DetailView):
    model = Producto
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ecommerce:producto_list')
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ecommerce:producto_list')
class ProductoDeleteView(DeleteView):
    model = Producto
    success_url = reverse_lazy('ecommerce:producto_list')

# Cliente
class ClienteListView(ListView):
    model = Cliente
class ClienteDetailView(DetailView):
    model = Cliente
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('ecommerce:cliente_list')
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('ecommerce:cliente_list')
class ClienteDeleteView(DeleteView):
    model = Cliente
    success_url = reverse_lazy('ecommerce:cliente_list')

# Carrito
class CarritoListView(ListView):
    model = Carrito
class CarritoDetailView(DetailView):
    model = Carrito
class CarritoCreateView(CreateView):
    model = Carrito
    form_class = CarritoForm
    success_url = reverse_lazy('ecommerce:carrito_list')
class CarritoUpdateView(UpdateView):
    model = Carrito
    form_class = CarritoForm
    success_url = reverse_lazy('ecommerce:carrito_list')
class CarritoDeleteView(DeleteView):
    model = Carrito
    success_url = reverse_lazy('ecommerce:carrito_list')

# LineaCarrito
class LineaCarritoListView(ListView):
    model = LineaCarrito
class LineaCarritoDetailView(DetailView):
    model = LineaCarrito
class LineaCarritoCreateView(CreateView):
    model = LineaCarrito
    form_class = LineaCarritoForm
    success_url = reverse_lazy('ecommerce:lineacarrito_list')
class LineaCarritoUpdateView(UpdateView):
    model = LineaCarrito
    form_class = LineaCarritoForm
    success_url = reverse_lazy('ecommerce:lineacarrito_list')
class LineaCarritoDeleteView(DeleteView):
    model = LineaCarrito
    success_url = reverse_lazy('ecommerce:lineacarrito_list')

# Pedido
class PedidoListView(ListView):
    model = Pedido
class PedidoDetailView(DetailView):
    model = Pedido
class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('ecommerce:pedido_list')
class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('ecommerce:pedido_list')
class PedidoDeleteView(DeleteView):
    model = Pedido
    success_url = reverse_lazy('ecommerce:pedido_list')

# LineaPedido
class LineaPedidoListView(ListView):
    model = LineaPedido
class LineaPedidoDetailView(DetailView):
    model = LineaPedido
class LineaPedidoCreateView(CreateView):
    model = LineaPedido
    form_class = LineaPedidoForm
    success_url = reverse_lazy('ecommerce:lineapedido_list')
class LineaPedidoUpdateView(UpdateView):
    model = LineaPedido
    form_class = LineaPedidoForm
    success_url = reverse_lazy('ecommerce:lineapedido_list')
class LineaPedidoDeleteView(DeleteView):
    model = LineaPedido
    success_url = reverse_lazy('ecommerce:lineapedido_list')

# Pago
class PagoListView(ListView):
    model = Pago
class PagoDetailView(DetailView):
    model = Pago
class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy('ecommerce:pago_list')
class PagoUpdateView(UpdateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy('ecommerce:pago_list')
class PagoDeleteView(DeleteView):
    model = Pago
    success_url = reverse_lazy('ecommerce:pago_list')
