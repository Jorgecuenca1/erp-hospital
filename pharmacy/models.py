from django.db import models
from patients.models import Paciente
from professionals.models import ProfesionalSalud
from inventories.models import Producto # Los medicamentos serán productos en el inventario

class Medicamento(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True, help_text="Debe ser un producto de tipo 'Medicamento' en el inventario.")
    dosis = models.CharField(max_length=100, blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    requiere_receta = models.BooleanField(default=True)
    indicaciones_especiales = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.producto.nombre

class Receta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas')
    profesional_prescriptor = models.ForeignKey(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True, related_name='recetas_prescritas')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    instrucciones_generales = models.TextField(blank=True, null=True)
    fecha_caducidad = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Receta para {self.paciente.nombres} {self.paciente.apellidos} ({self.fecha_emision.strftime('%d/%m/%Y')})"

class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name='detalles_receta')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50, help_text="Ej: tabletas, ml, ampollas")
    dosis_indicada = models.CharField(max_length=200, help_text="Ej: 1 tableta cada 8 horas por 5 días")
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle de Receta'
        verbose_name_plural = 'Detalles de Receta'

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.medicamento.producto.nombre}"
