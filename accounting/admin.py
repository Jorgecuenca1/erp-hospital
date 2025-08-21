from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PeriodoContable, CuentaContable, Tercero, Diario, Impuesto, 
    AsientoContable, LineaAsiento, DatosEmpresa, CentroCosto, 
    ComprobanteContable, CertificadoRetencion, MovimientoBancario, CierreContable, Presupuesto,
    ReporteFiscal, DetalleFiscal, Pais, Departamento, Ciudad
)

# ========== CONFIGURACIÓN DE GRUPOS EN ADMIN ==========

# Configurar títulos del admin
admin.site.site_header = "Sistema de Contabilidad - ERP Hospitalario"
admin.site.site_title = "Contabilidad"
admin.site.index_title = "Gestión Contable Integral"

# ========== EMPRESAS ==========

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']
    
    class Meta:
        verbose_name = "🌍 País"
        verbose_name_plural = "🌍 EMPRESAS - Países"

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'pais']
    list_filter = ['pais']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']
    
    class Meta:
        verbose_name = "🏛️ Departamento"
        verbose_name_plural = "🏛️ EMPRESAS - Departamentos"

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'departamento']
    list_filter = ['departamento__pais', 'departamento']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']
    
    class Meta:
        verbose_name = "🏙️ Ciudad"
        verbose_name_plural = "🏙️ EMPRESAS - Ciudades"

@admin.register(DatosEmpresa)
class DatosEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'ciudad', 'representante_legal', 'cargo_representante']
    search_fields = ['nombre', 'nit', 'representante_legal']
    list_editable = ['ciudad', 'cargo_representante']
    
    class Meta:
        verbose_name = "🏢 Datos de Empresa"
        verbose_name_plural = "🏢 EMPRESAS - Datos de Empresa"

@admin.register(Tercero)
class TerceroAdmin(admin.ModelAdmin):
    list_display = ['nit', 'nombre', 'tipo', 'regimen_iva', 'ciudad', 'telefono', 'activa']
    list_filter = ['tipo', 'regimen_iva', 'activa', 'ciudad']
    search_fields = ['nit', 'nombre', 'primer_nombre', 'primer_apellido', 'razon_social']
    list_editable = ['activa']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('tipo', 'nombre', 'nit', 'codigo_tercero')
        }),
        ('Persona Natural', {
            'fields': ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido'),
            'classes': ('collapse',)
        }),
        ('Persona Jurídica', {
            'fields': ('razon_social',),
            'classes': ('collapse',)
        }),
        ('Ubicación', {
            'fields': ('pais', 'departamento', 'ciudad_nueva', 'direccion', 'ciudad')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email')
        }),
        ('Información Tributaria', {
            'fields': ('regimen_iva', 'responsable_ica')
        }),
        ('Información Financiera', {
            'fields': ('cupo_credito',)
        }),
        ('Estado', {
            'fields': ('activa',)
        })
    )
    
    class Meta:
        verbose_name = "👤 Tercero"
        verbose_name_plural = "👤 EMPRESAS - Terceros"

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
    
    class Meta:
        verbose_name = "🎯 Centro de Costo"
        verbose_name_plural = "🎯 EMPRESAS - Centros de Costo"

# ========== COMPROBANTES ==========

class LineaAsientoInline(admin.TabularInline):
    model = LineaAsiento
    extra = 1
    fields = ['cuenta', 'descripcion', 'debito', 'credito', 'impuesto', 'tercero', 'centro_costo']

@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'descripcion', 'diario', 'periodo', 'tercero', 'centro_costo', 'creado_por', 'total_debito', 'total_credito', 'balanceado']
    list_filter = ['fecha', 'diario', 'periodo', 'centro_costo', 'creado_por']
    search_fields = ['descripcion', 'referencia']
    date_hierarchy = 'fecha'
    inlines = [LineaAsientoInline]
    readonly_fields = ['fecha_creacion', 'creado_por']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('fecha', 'descripcion', 'diario', 'periodo')
        }),
        ('Asignación', {
            'fields': ('tercero', 'centro_costo', 'comprobante', 'referencia')
        }),
        ('Control', {
            'fields': ('creado_por', 'fecha_creacion'),
            'classes': ('collapse',)
        })
    )
    
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

    class Meta:
        verbose_name = "📋 Asiento Contable"
        verbose_name_plural = "📋 COMPROBANTES - Asientos Contables"

@admin.register(ComprobanteContable)
class ComprobanteContableAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'fecha', 'tercero', 'centro_costo', 'valor', 'estado', 'estado_color']
    list_filter = ['tipo', 'estado', 'fecha', 'centro_costo']
    search_fields = ['numero', 'tercero__numero_documento', 'descripcion']
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

    class Meta:
        verbose_name = "📄 Comprobante Contable"
        verbose_name_plural = "📄 COMPROBANTES - Comprobantes Contables"

@admin.register(LineaAsiento)
class LineaAsientoAdmin(admin.ModelAdmin):
    list_display = ['asiento', 'cuenta', 'descripcion', 'debito', 'credito', 'impuesto', 'tercero', 'centro_costo']
    list_filter = ['cuenta', 'impuesto', 'centro_costo', 'asiento__diario', 'asiento__periodo']
    search_fields = ['descripcion', 'cuenta__nombre', 'asiento__descripcion']
    list_editable = ['debito', 'credito']
    
    class Meta:
        verbose_name = "📝 Línea de Asiento"
        verbose_name_plural = "📝 COMPROBANTES - Líneas de Asiento"

# ========== REPORTES ==========

@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'activo', 'descripcion_tipo']
    list_filter = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']
    ordering = ['codigo']
    
    def descripcion_tipo(self, obj):
        descripciones = {
            'GENERAL': 'Registros contables generales - Usado para asientos manuales y ajustes',
            'CAJA': 'Movimientos de efectivo - Ingresos y egresos en efectivo',
            'BANCO': 'Movimientos bancarios - Transferencias, cheques, consignaciones',
            'VENTAS': 'Registro de ventas - Facturas de venta y servicios prestados',
            'COMPRAS': 'Registro de compras - Facturas de proveedores y gastos'
        }
        return descripciones.get(obj.tipo, 'Descripción no disponible')
    descripcion_tipo.short_description = '¿Qué hace este diario?'
    
    class Meta:
        verbose_name = "📊 Diario Contable"
        verbose_name_plural = "📊 REPORTES - Diarios Contables"

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
    
    class Meta:
        verbose_name = "📅 Período Contable"
        verbose_name_plural = "📅 REPORTES - Períodos Contables"

@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'nivel', 'padre', 'activa']
    list_filter = ['tipo', 'nivel', 'activa', 'padre']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activa']
    ordering = ['codigo']
    
    class Meta:
        verbose_name = "🏦 Cuenta Contable PUC"
        verbose_name_plural = "🏦 REPORTES - Plan Único de Cuentas (PUC)"

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
    
    class Meta:
        verbose_name = "🏧 Movimiento Bancario"
        verbose_name_plural = "🏧 REPORTES - Movimientos Bancarios"

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
    
    class Meta:
        verbose_name = "🔒 Cierre Contable"
        verbose_name_plural = "🔒 REPORTES - Cierres Contables"

# ========== IMPUESTOS ==========

@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'tipo', 'porcentaje', 'inicio_vigencia', 'fin_vigencia', 'valor_base_minimo', 'activo']
    list_filter = ['tipo', 'activo', 'inicio_vigencia']
    search_fields = ['nombre', 'codigo']
    list_editable = ['activo', 'porcentaje']
    ordering = ['codigo']
    date_hierarchy = 'inicio_vigencia'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'tipo')
        }),
        ('Configuración Tributaria', {
            'fields': ('porcentaje', 'valor_base_minimo')
        }),
        ('Vigencia', {
            'fields': ('inicio_vigencia', 'fin_vigencia')
        }),
        ('Estado', {
            'fields': ('activo',)
        })
    )
    
    class Meta:
        verbose_name = "💰 Impuesto"
        verbose_name_plural = "💰 IMPUESTOS - Configuración de Impuestos"

@admin.register(CertificadoRetencion)
class CertificadoRetencionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'fecha', 'tercero', 'base_gravable', 'porcentaje_retencion', 'valor_retenido']
    list_filter = ['tipo', 'fecha']
    search_fields = ['numero', 'tercero__numero_documento', 'concepto']
    list_editable = ['porcentaje_retencion']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha_creacion', 'creado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        obj.calcular_retencion()
        super().save_model(request, obj, form, change)
    
    class Meta:
        verbose_name = "📋 Certificado de Retención"
        verbose_name_plural = "📋 IMPUESTOS - Certificados de Retención"

# ========== PRESUPUESTO ==========

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['periodo', 'cuenta', 'centro_costo', 'tipo_presupuesto', 'monto_presupuestado', 'monto_real', 'variacion_porcentual_display', 'estado_color']
    list_filter = ['periodo', 'cuenta__tipo', 'centro_costo', 'tipo_presupuesto']
    search_fields = ['cuenta__codigo', 'cuenta__nombre', 'centro_costo__nombre']
    list_editable = ['monto_presupuestado']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'creado_por']
    
    fieldsets = (
        ('Configuración', {
            'fields': ('periodo', 'cuenta', 'centro_costo', 'tipo_presupuesto')
        }),
        ('Montos', {
            'fields': ('monto_presupuestado', 'monto_real')
        }),
        ('Control', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        })
    )
    
    def variacion_porcentual_display(self, obj):
        return f"{obj.variacion_porcentual():.2f}%"
    variacion_porcentual_display.short_description = 'Variación %'
    
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
    
    class Meta:
        verbose_name = "💹 Presupuesto"
        verbose_name_plural = "💹 PRESUPUESTO - Gestión Presupuestal"

# ========== REPORTES FISCALES ==========

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
    
    class Meta:
        verbose_name = "📊 Reporte Fiscal"
        verbose_name_plural = "📊 IMPUESTOS - Reportes Fiscales"

@admin.register(DetalleFiscal)
class DetalleFiscalAdmin(admin.ModelAdmin):
    list_display = ['reporte', 'fecha', 'tercero', 'concepto', 'base_gravable', 'valor_impuesto']
    list_filter = ['reporte__tipo', 'fecha', 'reporte__periodo']
    search_fields = ['tercero__numero_documento', 'concepto', 'reporte__tipo']
    date_hierarchy = 'fecha'
    
    class Meta:
        verbose_name = "📋 Detalle Fiscal"
        verbose_name_plural = "📋 IMPUESTOS - Detalles Fiscales"
