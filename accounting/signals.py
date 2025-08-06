from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AsientoContable, LineaAsiento, CuentaContable

@receiver(pre_save, sender=AsientoContable)
def validar_asiento_contable(sender, instance, **kwargs):
    """
    Valida que el asiento contable esté balanceado antes de guardarlo
    """
    if instance.pk:  # Solo para asientos existentes
        lineas = LineaAsiento.objects.filter(asiento=instance)
        total_debito = sum(linea.debito for linea in lineas)
        total_credito = sum(linea.credito for linea in lineas)
        
        if abs(total_debito - total_credito) > 0.01:  # Tolerancia de 1 centavo
            raise ValueError(f"El asiento no está balanceado. Débito: {total_debito}, Crédito: {total_credito}")

@receiver(post_save, sender=CuentaContable)
def actualizar_codigo_cuenta(sender, instance, created, **kwargs):
    """
    Actualiza automáticamente el código de las subcuentas cuando se modifica una cuenta padre
    """
    if not created and instance.padre:
        # Actualizar códigos de subcuentas si es necesario
        subcuentas = CuentaContable.objects.filter(padre=instance)
        for subcuenta in subcuentas:
            if not subcuenta.codigo.startswith(instance.codigo):
                # Aquí se podría implementar lógica para actualizar códigos
                pass

@receiver(post_save, sender=LineaAsiento)
def validar_linea_asiento(sender, instance, created, **kwargs):
    """
    Valida que una línea de asiento tenga débito o crédito, pero no ambos
    """
    if created or instance.pk:
        if instance.debito > 0 and instance.credito > 0:
            raise ValueError("Una línea no puede tener débito y crédito simultáneamente")
        
        if instance.debito == 0 and instance.credito == 0:
            raise ValueError("Una línea debe tener débito o crédito") 