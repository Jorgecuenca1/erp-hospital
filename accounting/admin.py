from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PeriodoContable, CuentaContable, Tercero, Diario, Impuesto, 
    AsientoContable, LineaAsiento, DatosEmpresa, CentroCosto, 
    ComprobanteContable, CertificadoRetencion, MovimientoBancario, CierreContable, Presupuesto,
    ReporteFiscal, DetalleFiscal
)

@admin.register(PeriodoContable)
class PeriodoContableAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin', 'cerrado', 'estado_color']
    list_filter = ['cerrado', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_inicio'
    
    def estado_color(self, obj):
        if obj.cerrado:
            return format_html('<span style="color: red;">❌ Cerrado</span>')
        return format_html('<span style="color: green;">✅ Abierto</span>')
    estado_color.short_description = 'Estado'

@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'nivel', 'padre', 'activa']
    list_filter = ['tipo', 'nivel', 'activa', 'padre']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activa']
    ordering = ['codigo']

@admin.register(Tercero)
class TerceroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'tipo', 'ciudad', 'telefono', 'email', 'activa']
    list_filter = ['tipo', 'ciudad', 'activa']
    search_fields = ['nombre', 'nit', 'email']
    list_editable = ['activa']
    ordering = ['nombre']

@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']
    ordering = ['codigo']

@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'porcentaje', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'codigo']
    list_editable = ['activo', 'porcentaje']
    ordering = ['nombre']

class LineaAsientoInline(admin.TabularInline):
    model = LineaAsiento
    extra = 1
    fields = ['cuenta', 'descripcion', 'debito', 'credito', 'impuesto', 'tercero']

@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'descripcion', 'diario', 'periodo', 'tercero', 'creado_por', 'total_debito', 'total_credito', 'balanceado']
    list_filter = ['fecha', 'diario', 'periodo', 'creado_por']
    search_fields = ['descripcion', 'referencia']
    date_hierarchy = 'fecha'
    inlines = [LineaAsientoInline]
    readonly_fields = ['fecha_creacion', 'creado_por']
    
    def total_debito(self, obj):
        return sum(linea.debito for linea in obj.lineas.all())
    total_debito.short_description = 'Total Débito'
    
    def total_credito(self, obj):
        return sum(linea.credito for linea in obj.lineas.all())
    total_credito.short_description = 'Total Crédito'
    
    def balanceado(self, obj):
        debito = sum(linea.debito for linea in obj.lineas.all())
        credito = sum(linea.credito for linea in obj.lineas.all())
        if debito == credito:
            return format_html('<span style="color: green;">✅ Balanceado</span>')
        return format_html('<span style="color: red;">❌ Desbalanceado</span>')
    balanceado.short_description = 'Balance'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(LineaAsiento)
class LineaAsientoAdmin(admin.ModelAdmin):
    list_display = ['asiento', 'cuenta', 'descripcion', 'debito', 'credito', 'impuesto', 'tercero']
    list_filter = ['cuenta', 'impuesto', 'asiento__diario', 'asiento__periodo']
    search_fields = ['descripcion', 'cuenta__nombre', 'asiento__descripcion']
    list_editable = ['debito', 'credito']

@admin.register(DatosEmpresa)
class DatosEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'ciudad', 'representante_legal', 'cargo_representante']
    search_fields = ['nombre', 'nit', 'representante_legal']
    list_editable = ['ciudad', 'cargo_representante']

@admin.register(CentroCosto)
class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'contrato', 'fecha_inicio', 'fecha_fin', 'activo', 'estado_color']
    list_filter = ['activo', 'fecha_inicio', 'fecha_fin']
    search_fields = ['codigo', 'nombre', 'contrato']
    list_editable = ['activo']
    date_hierarchy = 'fecha_inicio'
    
    def estado_color(self, obj):
        if obj.activo:
            return format_html('<span style="color: green;">✅ Activo</span>')
        return format_html('<span style="color: red;">❌ Inactivo</span>')
    estado_color.short_description = 'Estado'

@admin.register(ComprobanteContable)
class ComprobanteContableAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'fecha', 'tercero', 'valor', 'estado', 'estado_color']
    list_filter = ['tipo', 'estado', 'fecha', 'centro_costo']
    search_fields = ['numero', 'tercero__nombre', 'descripcion']
    list_editable = ['estado']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'creado_por']
    
    def estado_color(self, obj):
        if obj.estado == 'ACTIVO':
            return format_html('<span style="color: green;">✅ Activo</span>')
        elif obj.estado == 'ANULADO':
            return format_html('<span style="color: red;">❌ Anulado</span>')
        else:
            return format_html('<span style="color: orange;">⏳ Sin Procesar</span>')
    estado_color.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(CertificadoRetencion)
class CertificadoRetencionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'fecha', 'tercero', 'base_gravable', 'porcentaje_retencion', 'valor_retenido']
    list_filter = ['tipo', 'fecha']
    search_fields = ['numero', 'tercero__nombre', 'concepto']
    list_editable = ['porcentaje_retencion']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha_creacion', 'creado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        obj.calcular_retencion()
        super().save_model(request, obj, form, change)

# Nuevos admin para funcionalidades agregadas
@admin.register(MovimientoBancario)
class MovimientoBancarioAdmin(admin.ModelAdmin):
    list_display = ['banco', 'cuenta_bancaria', 'fecha', 'descripcion', 'valor', 'tipo', 'conciliado', 'estado_color']
    list_filter = ['banco', 'tipo', 'conciliado', 'fecha']
    search_fields = ['descripcion', 'referencia', 'banco']
    list_editable = ['conciliado']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha_creacion', 'creado_por']
    
    def estado_color(self, obj):
        if obj.conciliado:
            return format_html('<span style="color: green;">✅ Conciliado</span>')
        return format_html('<span style="color: orange;">⏳ Pendiente</span>')
    estado_color.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(CierreContable)
class CierreContableAdmin(admin.ModelAdmin):
    list_display = ['periodo', 'fecha_cierre', 'cerrado_por', 'activo', 'estado_color']
    list_filter = ['activo', 'fecha_cierre', 'periodo']
    search_fields = ['periodo__nombre', 'observaciones']
    list_editable = ['activo']
    date_hierarchy = 'fecha_cierre'
    readonly_fields = ['fecha_cierre', 'cerrado_por']
    
    def estado_color(self, obj):
        if obj.activo:
            return format_html('<span style="color: green;">✅ Activo</span>')
        return format_html('<span style="color: red;">❌ Inactivo</span>')
    estado_color.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.cerrado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['periodo', 'cuenta', 'centro_costo', 'monto_presupuestado', 'monto_real', 'variacion_porcentual', 'estado_color']
    list_filter = ['periodo', 'cuenta__tipo', 'centro_costo']
    search_fields = ['cuenta__codigo', 'cuenta__nombre', 'centro_costo__nombre']
    list_editable = ['monto_presupuestado']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'creado_por']
    
    def variacion_porcentual(self, obj):
        return f"{obj.variacion_porcentual():.2f}%"
    variacion_porcentual.short_description = 'Variación %'
    
    def estado_color(self, obj):
        variacion = obj.variacion_porcentual()
        if variacion <= 5:
            return format_html('<span style="color: green;">✅ Dentro del presupuesto</span>')
        elif variacion <= 15:
            return format_html('<span style="color: orange;">⚠️ Atención</span>')
        else:
            return format_html('<span style="color: red;">❌ Excede presupuesto</span>')
    estado_color.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(ReporteFiscal)
class ReporteFiscalAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'periodo', 'fecha_inicio', 'fecha_fin', 'base_gravable', 'impuesto_a_pagar', 'estado', 'generado_por', 'fecha_generacion']
    list_filter = ['tipo', 'estado', 'periodo', 'fecha_generacion']
    search_fields = ['periodo__nombre', 'generado_por__username']
    readonly_fields = ['fecha_generacion', 'generado_por']
    list_editable = ['estado']
    date_hierarchy = 'fecha_generacion'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo si es nuevo
            obj.generado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(DetalleFiscal)
class DetalleFiscalAdmin(admin.ModelAdmin):
    list_display = ['reporte', 'fecha', 'tercero', 'concepto', 'base_gravable', 'valor_impuesto']
    list_filter = ['reporte__tipo', 'fecha', 'reporte__periodo']
    search_fields = ['tercero__nombre', 'concepto', 'reporte__tipo']
    date_hierarchy = 'fecha'
