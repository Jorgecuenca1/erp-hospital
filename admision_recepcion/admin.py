from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Municipio, Empresa, Convenio, Servicio, Prestador,
    OrdenServicio, DetalleOrdenServicio, SeguimientoPaciente, CitaEmpresarial, ListaPrecios, HistoriaClinica,
    FichaClinica, EvaluacionOcupacional, AntecedenteFamiliar, AntecedentePersonal, AntecedenteSistema,
    ExposicionLaboral, AccidenteLaboral, EnfermedadLaboral,
    ExamenVisual, AntecedenteVisual, DiagnosticoVisual, ConductaRecomendacionVisual,
    Audiometria, AntecedenteAuditivo, AntecedenteAuditivoLaboral, DiagnosticoAuditivo, RecomendacionAuditiva,
    Espirometria, RecomendacionEspirometria,
    EvaluacionOsteomuscular, RecomendacionOsteomuscular,
    HistoriaClinicaGeneral, AntecedenteFamiliarGeneral, AntecedentePersonalGeneral,
    DocumentoClinico, DiagnosticoGeneral, OrdenMedicamento, OrdenServicioGeneral,
    OrdenRemision, OrdenIncapacidad, CertificadoMedico, EvolucionGeneral
)


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'departamento', 'pais', 'activo']
    list_filter = ['activo', 'departamento', 'pais']
    search_fields = ['codigo', 'nombre', 'departamento']
    ordering = ['departamento', 'nombre']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nit', 'razon_social', 'tipo_empresa', 'telefono', 'email', 'activo']
    list_filter = ['tipo_empresa', 'activo']
    search_fields = ['nit', 'razon_social', 'nombre_comercial']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nit', 'razon_social', 'nombre_comercial', 'tipo_empresa')
        }),
        ('Contacto', {
            'fields': ('direccion', 'telefono', 'email', 'contacto_principal')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'empresa', 'fecha_inicio', 'fecha_fin', 'estado']
    list_filter = ['estado', 'fecha_inicio', 'fecha_fin']
    search_fields = ['codigo', 'nombre', 'empresa__razon_social']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'empresa')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Detalles', {
            'fields': ('valor_contrato', 'descripcion', 'observaciones')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'valor_base', 'requiere_autorizacion', 'activo']
    list_filter = ['tipo', 'requiere_autorizacion', 'activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'tipo')
        }),
        ('Configuración', {
            'fields': ('valor_base', 'requiere_autorizacion', 'activo')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'especialidad', 'telefono', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre', 'especialidad']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo', 'especialidad')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Auditoría', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


class DetalleOrdenServicioInline(admin.TabularInline):
    model = DetalleOrdenServicio
    extra = 1
    fields = ['cantidad', 'servicio', 'prestador', 'valor_unitario', 'forma_pago', 'valor_pagar']
    readonly_fields = []


class SeguimientoPacienteInline(admin.TabularInline):
    model = SeguimientoPaciente
    extra = 0
    fields = ['estado', 'fecha_estado', 'observaciones', 'usuario']
    readonly_fields = ['fecha_estado', 'usuario']


@admin.register(OrdenServicio)
class OrdenServicioAdmin(admin.ModelAdmin):
    list_display = [
        'numero_orden', 'get_nombre_completo', 'numero_identificacion', 
        'fecha_orden', 'estado_orden_colored', 'sede', 'total_pagar'
    ]
    list_filter = [
        'estado_orden', 'sede', 'fecha_orden', 'tipo_documento', 
        'genero', 'zona', 'convenio__empresa'
    ]
    search_fields = [
        'numero_orden', 'numero_identificacion', 'primer_nombre', 
        'primer_apellido', 'segundo_apellido'
    ]
    readonly_fields = [
        'numero_orden', 'total_orden', 'total_pagar', 
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'fecha_orden'
    inlines = [DetalleOrdenServicioInline, SeguimientoPacienteInline]
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('numero_orden', 'fecha_orden', 'estado_orden', 'created_by')
        }),
        ('Datos Personales', {
            'fields': (
                'tipo_documento', 'numero_identificacion', 'ciudad_nacimiento', 'fecha_nacimiento',
                'primer_apellido', 'segundo_apellido', 'primer_nombre', 'otros_nombres',
                'genero', 'estado_civil', 'nivel_educativo', 'correo_electronico'
            )
        }),
        ('Archivos', {
            'fields': ('foto', 'huella', 'firma'),
            'classes': ('collapse',)
        }),
        ('Datos de Ubicación', {
            'fields': (
                'zona', 'direccion', 'barrio', 'localidad', 'sede', 
                'estrato', 'municipio', 'celulares', 'telefonos'
            )
        }),
        ('Datos de Trabajo', {
            'fields': (
                'profesion_cargo', 'funciones_cargo', 'tipo_evaluacion',
                'convenio', 'empresa_mision', 'eps', 'afp', 'arl'
            )
        }),
        ('Observaciones', {
            'fields': ('observaciones', 'fecha_solicitud')
        }),
        ('Totales', {
            'fields': ('total_orden', 'total_pagar'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_nombre_completo(self, obj):
        return obj.nombre_completo
    get_nombre_completo.short_description = 'Nombre Completo'
    
    def estado_orden_colored(self, obj):
        colors = {
            'PENDIENTE': 'orange',
            'AUTORIZADA': 'blue',
            'EN_PROCESO': 'purple',
            'COMPLETADA': 'green',
            'CANCELADA': 'red',
            'FACTURADA': 'darkgreen'
        }
        color = colors.get(obj.estado_orden, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_orden_display()
        )
    estado_orden_colored.short_description = 'Estado'
    
    actions = ['marcar_como_autorizada', 'marcar_como_en_proceso', 'marcar_como_completada']
    
    def marcar_como_autorizada(self, request, queryset):
        updated = queryset.update(estado_orden='AUTORIZADA')
        self.message_user(request, f'{updated} órdenes marcadas como autorizadas.')
    marcar_como_autorizada.short_description = "Marcar como autorizada"
    
    def marcar_como_en_proceso(self, request, queryset):
        updated = queryset.update(estado_orden='EN_PROCESO')
        self.message_user(request, f'{updated} órdenes marcadas como en proceso.')
    marcar_como_en_proceso.short_description = "Marcar como en proceso"
    
    def marcar_como_completada(self, request, queryset):
        updated = queryset.update(estado_orden='COMPLETADA')
        self.message_user(request, f'{updated} órdenes marcadas como completadas.')
    marcar_como_completada.short_description = "Marcar como completada"


@admin.register(DetalleOrdenServicio)
class DetalleOrdenServicioAdmin(admin.ModelAdmin):
    list_display = [
        'orden', 'servicio', 'prestador', 'cantidad', 
        'valor_unitario', 'valor_total', 'forma_pago', 'autorizado'
    ]
    list_filter = ['forma_pago', 'autorizado', 'servicio__tipo']
    search_fields = [
        'orden__numero_orden', 'servicio__nombre', 'prestador__nombre'
    ]
    readonly_fields = ['created_at']
    
    def valor_total(self, obj):
        return obj.valor_total
    valor_total.short_description = 'Valor Total'


@admin.register(SeguimientoPaciente)
class SeguimientoPacienteAdmin(admin.ModelAdmin):
    list_display = ['orden', 'estado', 'fecha_estado', 'usuario']
    list_filter = ['estado', 'fecha_estado']
    search_fields = ['orden__numero_orden', 'orden__primer_nombre', 'orden__primer_apellido']
    readonly_fields = ['fecha_estado']
    date_hierarchy = 'fecha_estado'


@admin.register(CitaEmpresarial)
class CitaEmpresarialAdmin(admin.ModelAdmin):
    list_display = [
        'numero_cita', 'fecha_cita', 'hora_cita', 'nombre_trabajador', 
        'empresa', 'estado', 'tipo_servicio', 'sede_cita'
    ]
    list_filter = [
        'estado', 'fecha_cita', 'sede_cita', 'tipo_servicio', 
        'empresa', 'programada_por_portal'
    ]
    search_fields = [
        'numero_cita', 'numero_identificacion', 'nombre_trabajador', 
        'empresa__razon_social', 'empresa__nit'
    ]
    readonly_fields = [
        'numero_cita', 'fecha_programacion', 'fecha_confirmacion', 
        'fecha_cancelacion', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'fecha_cita'
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': (
                'numero_cita', 'fecha_cita', 'hora_cita', 'estado', 'sede_cita'
            )
        }),
        ('Información del Trabajador', {
            'fields': (
                'tipo_documento', 'numero_identificacion', 'nombre_trabajador',
                'telefono_trabajador', 'email_trabajador'
            )
        }),
        ('Información de la Empresa', {
            'fields': (
                'empresa', 'contacto_empresa', 'telefono_empresa', 'email_empresa'
            )
        }),
        ('Información del Servicio', {
            'fields': (
                'tipo_servicio', 'servicios_adicionales', 'observaciones_servicio',
                'prestador_asignado', 'valor_estimado'
            )
        }),
        ('Autorizaciones', {
            'fields': (
                'requiere_autorizacion', 'numero_autorizacion'
            ),
            'classes': ('collapse',)
        }),
        ('Confirmación y Cancelación', {
            'fields': (
                'fecha_confirmacion', 'confirmada_por', 'fecha_cancelacion',
                'motivo_cancelacion', 'cancelada_por'
            ),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': (
                'fecha_programacion', 'programada_por_portal', 'ip_origen',
                'orden_servicio', 'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['servicios_adicionales']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'empresa', 'prestador_asignado', 'confirmada_por', 'cancelada_por', 'orden_servicio'
        )
    
    actions = ['confirmar_citas', 'cancelar_citas']
    
    def confirmar_citas(self, request, queryset):
        """Confirmar citas seleccionadas"""
        confirmadas = 0
        for cita in queryset:
            if cita.puede_confirmar:
                cita.confirmar_cita(request.user)
                confirmadas += 1
        
        self.message_user(
            request,
            f"{confirmadas} cita(s) confirmada(s) exitosamente."
        )
    confirmar_citas.short_description = "Confirmar citas seleccionadas"
    
    def cancelar_citas(self, request, queryset):
        """Cancelar citas seleccionadas"""
        canceladas = 0
        for cita in queryset:
            if cita.puede_cancelar:
                cita.cancelar_cita("Cancelada desde administración", request.user)
                canceladas += 1
        
        self.message_user(
            request,
            f"{canceladas} cita(s) cancelada(s) exitosamente."
        )
    cancelar_citas.short_description = "Cancelar citas seleccionadas"


@admin.register(ListaPrecios)
class ListaPreciosAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_interno', 'nombre_producto_servicio', 'categoria', 
        'precio_formatted', 'codigo_cups', 'tipo_rips', 'iva_formatted', 'activo'
    ]
    list_filter = [
        'categoria', 'tipo_rips', 'activo', 'gravado_iva', 
        'requiere_autorizacion', 'generar_rips'
    ]
    search_fields = [
        'codigo_interno', 'nombre_producto_servicio', 'codigo_cups', 
        'codigo_cum', 'codigo_cie10', 'descripcion'
    ]
    readonly_fields = [
        'codigo_interno', 'created_at', 'updated_at', 'precio_con_iva_display'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'codigo_interno', 'nombre_producto_servicio', 'descripcion', 'categoria'
            )
        }),
        ('Precios', {
            'fields': (
                'precio', 'precio_convenio', 'precio_particular', 'precio_con_iva_display'
            )
        }),
        ('Códigos de Facturación', {
            'fields': (
                'codigo_cups', 'codigo_soat', 'codigo_iss', 'codigo_cum', 'codigo_cie10'
            )
        }),
        ('RIPS', {
            'fields': (
                'tipo_rips', 'generar_rips'
            )
        }),
        ('Impuestos', {
            'fields': (
                'porcentaje_iva', 'gravado_iva'
            )
        }),
        ('Convenios y Precios Especiales', {
            'fields': (
                'convenios', 'precio_por_convenio'
            ),
            'classes': ('collapse',)
        }),
        ('Control de Estado', {
            'fields': (
                'activo', 'requiere_autorizacion', 'ambulatorio', 'hospitalario'
            )
        }),
        ('Información Adicional', {
            'fields': (
                'unidad_medida', 'tiempo_estimado', 'observaciones'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_by', 'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['convenios']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by').prefetch_related('convenios')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo al crear
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def precio_formatted(self, obj):
        return f"${obj.precio:,.0f}"
    precio_formatted.short_description = 'Precio'
    precio_formatted.admin_order_field = 'precio'
    
    def iva_formatted(self, obj):
        if obj.gravado_iva:
            return f"{obj.porcentaje_iva}%"
        return "0.00%"
    iva_formatted.short_description = 'IVA'
    iva_formatted.admin_order_field = 'porcentaje_iva'
    
    def precio_con_iva_display(self, obj):
        precio_con_iva = obj.get_precio_con_iva()
        return f"${precio_con_iva:,.0f}"
    precio_con_iva_display.short_description = 'Precio con IVA'
    
    actions = ['activar_productos', 'desactivar_productos', 'aplicar_iva']
    
    def activar_productos(self, request, queryset):
        """Activar productos seleccionados"""
        count = queryset.update(activo=True)
        self.message_user(request, f"{count} producto(s) activado(s) exitosamente.")
    activar_productos.short_description = "Activar productos seleccionados"
    
    def desactivar_productos(self, request, queryset):
        """Desactivar productos seleccionados"""
        count = queryset.update(activo=False)
        self.message_user(request, f"{count} producto(s) desactivado(s) exitosamente.")
    desactivar_productos.short_description = "Desactivar productos seleccionados"
    
    def aplicar_iva(self, request, queryset):
        """Aplicar IVA del 19% a productos seleccionados"""
        count = queryset.update(gravado_iva=True, porcentaje_iva=19)
        self.message_user(request, f"IVA del 19% aplicado a {count} producto(s).")
    aplicar_iva.short_description = "Aplicar IVA 19% a productos seleccionados"


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = [
        'numero_hc', 'fecha_creacion', 'nombre_paciente', 'numero_identificacion',
        'empresa', 'tipo_examen', 'profesional', 'estado'
    ]
    list_filter = [
        'estado', 'tipo_examen', 'empresa', 'profesional', 
        'fecha_creacion', 'genero'
    ]
    search_fields = [
        'numero_hc', 'numero_identificacion', 'nombre_paciente',
        'empresa__razon_social', 'profesional__nombre'
    ]
    readonly_fields = [
        'numero_hc', 'fecha_creacion', 'updated_at', 'edad_display',
        'fecha_cierre', 'fecha_anulacion'
    ]
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información de la Historia', {
            'fields': (
                'numero_hc', 'fecha_creacion', 'estado', 'orden_servicio'
            )
        }),
        ('Datos del Paciente', {
            'fields': (
                'tipo_documento', 'numero_identificacion', 'nombre_paciente',
                'fecha_nacimiento', 'edad_display', 'genero', 'telefono', 'email', 'direccion'
            )
        }),
        ('Información Empresarial', {
            'fields': (
                'empresa', 'cargo'
            )
        }),
        ('Información del Examen', {
            'fields': (
                'tipo_examen', 'profesional'
            )
        }),
        ('Historia Médica', {
            'fields': (
                'motivo_consulta', 'antecedentes_personales', 'antecedentes_familiares',
                'antecedentes_ocupacionales', 'revision_sistemas'
            ),
            'classes': ('collapse',)
        }),
        ('Examen Físico', {
            'fields': (
                'signos_vitales', 'examen_fisico'
            ),
            'classes': ('collapse',)
        }),
        ('Resultados de Exámenes', {
            'fields': (
                'laboratorios', 'imagenes', 'otros_examenes'
            ),
            'classes': ('collapse',)
        }),
        ('Diagnósticos', {
            'fields': (
                'diagnostico_principal', 'diagnosticos_secundarios', 'aptitud_laboral'
            ),
            'classes': ('collapse',)
        }),
        ('Recomendaciones y Tratamiento', {
            'fields': (
                'recomendaciones', 'tratamiento', 'incapacidad_dias', 'restricciones'
            ),
            'classes': ('collapse',)
        }),
        ('Control de Estado', {
            'fields': (
                'fecha_cierre', 'cerrada_por', 'motivo_anulacion',
                'fecha_anulacion', 'anulada_por'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_by', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'empresa', 'profesional', 'created_by', 'cerrada_por', 'anulada_por'
        )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo al crear
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def edad_display(self, obj):
        if obj.edad:
            return f"{obj.edad} años"
        return "No disponible"
    edad_display.short_description = 'Edad'
    
    actions = ['cerrar_historias', 'reabrir_historias', 'anular_historias']
    
    def cerrar_historias(self, request, queryset):
        """Cerrar historias seleccionadas"""
        count = 0
        for historia in queryset:
            if historia.puede_cerrar:
                historia.cerrar_historia(request.user)
                count += 1
        
        self.message_user(request, f"{count} historia(s) cerrada(s) exitosamente.")
    cerrar_historias.short_description = "Cerrar historias seleccionadas"
    
    def reabrir_historias(self, request, queryset):
        """Reabrir historias seleccionadas"""
        count = 0
        for historia in queryset:
            if historia.puede_reabrir:
                historia.reabrir_historia()
                count += 1
        
        self.message_user(request, f"{count} historia(s) reabierta(s) exitosamente.")
    reabrir_historias.short_description = "Reabrir historias seleccionadas"
    
    def anular_historias(self, request, queryset):
        """Anular historias seleccionadas"""
        count = 0
        for historia in queryset:
            if historia.puede_anular:
                historia.anular_historia("Anulada desde administración", request.user)
                count += 1
        
        self.message_user(request, f"{count} historia(s) anulada(s) exitosamente.")
    anular_historias.short_description = "Anular historias seleccionadas"


# ===== FICHAS CLÍNICAS =====

class AntecedenteFamiliarInline(admin.TabularInline):
    model = AntecedenteFamiliar
    extra = 0
    readonly_fields = ['fecha_registro']


class AntecedentePersonalInline(admin.TabularInline):
    model = AntecedentePersonal
    extra = 0
    readonly_fields = ['fecha_registro']


class AntecedenteSistemaInline(admin.TabularInline):
    model = AntecedenteSistema
    extra = 0


class ExposicionLaboralInline(admin.TabularInline):
    model = ExposicionLaboral
    extra = 0
    readonly_fields = ['fecha_registro']


class AccidenteLaboralInline(admin.TabularInline):
    model = AccidenteLaboral
    extra = 0
    readonly_fields = ['fecha_registro']


class EnfermedadLaboralInline(admin.TabularInline):
    model = EnfermedadLaboral
    extra = 0
    readonly_fields = ['fecha_registro']


@admin.register(EvaluacionOcupacional)
class EvaluacionOcupacionalAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'tipo_evaluacion', 'actividad_economica',
        'estado_civil', 'eps', 'arl'
    ]
    list_filter = [
        'tipo_evaluacion', 'estado_civil', 'nivel_educativo',
        'jornada_laboral', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'actividad_economica', 'eps', 'arl'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'tipo_evaluacion', 'actividad_economica'
            )
        }),
        ('Datos Personales', {
            'fields': (
                'estado_civil', 'nivel_educativo', 'eps', 'afp', 'arl',
                'tipo_sangre', 'numero_hijos', 'ingresos_promedio', 'jornada_laboral'
            )
        }),
        ('Información Laboral', {
            'fields': (
                'area_cargo', 'profesion_cargo', 'funciones_cargo', 'motivo_consulta'
            )
        }),
        ('Elementos de Protección Personal', {
            'fields': (
                'epp_casco', 'epp_gorro', 'epp_respirador', 'epp_gafas',
                'epp_peto', 'epp_bata', 'epp_overol', 'epp_delantal_plomo',
                'epp_ropa_termica', 'epp_auditivos', 'epp_careta', 'epp_tapabocas',
                'epp_guantes', 'epp_cinturon', 'epp_botas', 'epp_polainas', 'epp_otros'
            ),
            'classes': ('collapse',)
        }),
        ('Examen Médico', {
            'fields': (
                'historia_antecedentes', 'revision_sistemas', 'signos_vitales',
                'anexo_alturas', 'anexo_osteomuscular', 'paraclinicos_diagnosticos',
                'concepto_aptitud', 'ordenes_medicas', 'evoluciones_notas'
            ),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': (
                'observaciones_adicionales',
            )
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AntecedenteFamiliarInline,
        AntecedentePersonalInline,
        AntecedenteSistemaInline,
        ExposicionLaboralInline,
        AccidenteLaboralInline,
        EnfermedadLaboralInline,
    ]


@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = [
        'numero_ficha', 'tipo_ficha', 'nombre_trabajador', 'numero_identificacion',
        'empresa', 'fecha_evaluacion', 'estado', 'profesional_evaluador'
    ]
    list_filter = [
        'tipo_ficha', 'estado', 'empresa', 'profesional_evaluador',
        'fecha_creacion', 'fecha_evaluacion'
    ]
    search_fields = [
        'numero_ficha', 'numero_identificacion', 'nombre_trabajador',
        'empresa__razon_social'
    ]
    readonly_fields = [
        'numero_ficha', 'fecha_creacion', 'updated_at'
    ]
    date_hierarchy = 'fecha_evaluacion'
    
    fieldsets = (
        ('Información de la Ficha', {
            'fields': (
                'numero_ficha', 'tipo_ficha', 'fecha_creacion', 'fecha_evaluacion', 'estado'
            )
        }),
        ('Datos del Trabajador', {
            'fields': (
                'numero_identificacion', 'tipo_documento', 'nombre_trabajador',
                'fecha_nacimiento', 'genero', 'edad'
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'telefono', 'email', 'direccion', 'municipio'
            )
        }),
        ('Información Laboral', {
            'fields': (
                'empresa', 'cargo', 'profesional_evaluador'
            )
        }),
        ('Relaciones', {
            'fields': (
                'historia_clinica', 'orden_servicio'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_by', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'empresa', 'profesional_evaluador', 'municipio', 'created_by'
        )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo al crear
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Registro de modelos relacionados

@admin.register(AntecedenteFamiliar)
class AntecedenteFamiliarAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_ocupacional', 'patologia', 'parentesco', 'fecha_registro']
    list_filter = ['patologia', 'parentesco', 'fecha_registro']
    search_fields = ['evaluacion_ocupacional__ficha_clinica__nombre_trabajador']


@admin.register(AntecedentePersonal)
class AntecedentePersonalAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_ocupacional', 'tipo_antecedente', 'diagnostico_observaciones', 'fecha_registro']
    list_filter = ['tipo_antecedente', 'fecha_registro']
    search_fields = ['evaluacion_ocupacional__ficha_clinica__nombre_trabajador']


@admin.register(ExposicionLaboral)
class ExposicionLaboralAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_ocupacional', 'nombre_empresa', 'cargo', 'tiempo_exposicion_anos', 'fecha_registro']
    list_filter = ['fecha_registro']
    search_fields = ['nombre_empresa', 'cargo', 'evaluacion_ocupacional__ficha_clinica__nombre_trabajador']


@admin.register(AccidenteLaboral)
class AccidenteLaboralAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_ocupacional', 'nombre_empresa', 'tipo_accidente', 'fecha_accidente', 'reportado_arl']
    list_filter = ['reportado_arl', 'fecha_accidente', 'fecha_registro']
    search_fields = ['nombre_empresa', 'tipo_accidente', 'evaluacion_ocupacional__ficha_clinica__nombre_trabajador']


@admin.register(EnfermedadLaboral)
class EnfermedadLaboralAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_ocupacional', 'descripcion_enfermedad', 'fecha_diagnostico', 'fecha_registro']
    list_filter = ['fecha_diagnostico', 'fecha_registro']
    search_fields = ['descripcion_enfermedad', 'evaluacion_ocupacional__ficha_clinica__nombre_trabajador']


# ===== EXAMEN VISUAL =====

class AntecedenteVisualInline(admin.TabularInline):
    model = AntecedenteVisual
    extra = 0


class DiagnosticoVisualInline(admin.TabularInline):
    model = DiagnosticoVisual
    extra = 0


class ConductaRecomendacionVisualInline(admin.TabularInline):
    model = ConductaRecomendacionVisual
    extra = 0


@admin.register(ExamenVisual)
class ExamenVisualAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'sintomatologia', 'ultimo_examen',
        'created_at'
    ]
    list_filter = [
        'sintomatologia', 'via_ingreso', 'finalidad_consulta', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'motivo_consulta', 'diagnostico_recomendaciones'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'ultimo_examen', 'lugar_ultimo_examen', 'motivo_consulta'
            )
        }),
        ('Sintomatología', {
            'fields': (
                'sintomatologia',
            )
        }),
        ('Agudeza Visual Sin Corrección', {
            'fields': (
                ('ojo_derecho_vl_sc', 'ojo_derecho_vp_sc', 'ojo_derecho_ph_sc'),
                ('ojo_izquierdo_vl_sc', 'ojo_izquierdo_vp_sc', 'ojo_izquierdo_ph_sc'),
                ('ambos_ojos_vl_sc', 'ambos_ojos_vp_sc', 'ambos_ojos_ph_sc'),
            )
        }),
        ('Agudeza Visual Con Corrección', {
            'fields': (
                ('ojo_derecho_vl_cc', 'ojo_derecho_vp_cc'),
                ('ojo_izquierdo_vl_cc', 'ojo_izquierdo_vp_cc'),
                ('ambos_ojos_vl_cc', 'ambos_ojos_vp_cc'),
            )
        }),
        ('Examen Externo', {
            'fields': (
                'ojo_derecho_externo', 'ojo_izquierdo_externo'
            )
        }),
        ('Pruebas y Observaciones', {
            'fields': (
                'reflejos_observacion', 'vision_lejana_cover', 'vision_proxima_cover',
                'motilidad_observacion', 'convergencia_observacion'
            )
        }),
        ('Oftalmoscopía', {
            'fields': (
                'ojo_derecho_oftalmoscopia', 'ojo_izquierdo_oftalmoscopia'
            )
        }),
        ('Queratometría', {
            'fields': (
                'ojo_derecho_queratometria', 'ojo_izquierdo_queratometria'
            )
        }),
        ('Refracción', {
            'fields': (
                'ojo_derecho_refraccion_av', 'ojo_izquierdo_refraccion_av'
            )
        }),
        ('RX Final', {
            'fields': (
                ('ojo_derecho_rx_vl', 'ojo_derecho_rx_vp', 'ojo_derecho_rx_add'),
                ('ojo_izquierdo_rx_vl', 'ojo_izquierdo_rx_vp', 'ojo_izquierdo_rx_add'),
            )
        }),
        ('Visión Color y Estereopsis', {
            'fields': (
                'ojo_derecho_vision_color', 'ojo_izquierdo_vision_color', 'estereopsis_observacion'
            )
        }),
        ('Diagnósticos y Recomendaciones', {
            'fields': (
                'diagnostico_recomendaciones', 'otras_observaciones'
            )
        }),
        ('Información RIPS', {
            'fields': (
                'via_ingreso', 'finalidad_consulta', 'causa_externa'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AntecedenteVisualInline,
        DiagnosticoVisualInline,
        ConductaRecomendacionVisualInline,
    ]


# Registro de modelos relacionados del examen visual

@admin.register(AntecedenteVisual)
class AntecedenteVisualAdmin(admin.ModelAdmin):
    list_display = ['examen_visual', 'tipo_antecedente', 'observacion']
    list_filter = ['tipo_antecedente']
    search_fields = ['examen_visual__ficha_clinica__nombre_trabajador']


@admin.register(DiagnosticoVisual)
class DiagnosticoVisualAdmin(admin.ModelAdmin):
    list_display = ['examen_visual', 'tipo_diagnostico', 'codigo_cie10', 'nombre_diagnostico', 'lateralidad']
    list_filter = ['tipo_diagnostico', 'lateralidad', 'tipo_impresion']
    search_fields = ['codigo_cie10', 'nombre_diagnostico', 'examen_visual__ficha_clinica__nombre_trabajador']


@admin.register(ConductaRecomendacionVisual)
class ConductaRecomendacionVisualAdmin(admin.ModelAdmin):
    list_display = ['examen_visual', 'tipo_item', 'codigo', 'descripcion', 'seleccionado']
    list_filter = ['tipo_item', 'seleccionado']
    search_fields = ['codigo', 'descripcion', 'examen_visual__ficha_clinica__nombre_trabajador']


# ===== AUDIOMETRÍA =====

class AntecedenteAuditivoInline(admin.TabularInline):
    model = AntecedenteAuditivo
    extra = 0


class AntecedenteAuditivoLaboralInline(admin.TabularInline):
    model = AntecedenteAuditivoLaboral
    extra = 0


class DiagnosticoAuditivoInline(admin.TabularInline):
    model = DiagnosticoAuditivo
    extra = 0


class RecomendacionAuditivaInline(admin.TabularInline):
    model = RecomendacionAuditiva
    extra = 0


@admin.register(Audiometria)
class AudiometriaAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'uso_cabina_sonoamortiguada', 'severidad_od',
        'severidad_oi', 'created_at'
    ]
    list_filter = [
        'uso_cabina_sonoamortiguada', 'realizo_retest', 'severidad_od', 'severidad_oi',
        'via_ingreso', 'finalidad_consulta', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'marca_audiometro', 'observaciones'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'producto', 'funciones_cargo', 'eps'
            )
        }),
        ('Condiciones de la Prueba', {
            'fields': (
                'descanso_auditivo_horas', 'realizo_retest', 'uso_cabina_sonoamortiguada',
                'marca_audiometro', 'fecha_ultima_calibracion'
            )
        }),
        ('Otoscopia', {
            'fields': (
                'otoscopia_oido_izquierdo', 'otoscopia_oido_derecho'
            )
        }),
        ('Vía Aérea - Oído Derecho', {
            'fields': (
                ('va_od_250', 'va_od_500', 'va_od_1000', 'va_od_2000'),
                ('va_od_3000', 'va_od_4000', 'va_od_6000', 'va_od_8000'),
            )
        }),
        ('Vía Aérea - Oído Izquierdo', {
            'fields': (
                ('va_oi_250', 'va_oi_500', 'va_oi_1000', 'va_oi_2000'),
                ('va_oi_3000', 'va_oi_4000', 'va_oi_6000', 'va_oi_8000'),
            )
        }),
        ('Vía Ósea - Oído Derecho', {
            'fields': (
                ('vo_od_250', 'vo_od_500', 'vo_od_1000', 'vo_od_2000'),
                ('vo_od_3000', 'vo_od_4000', 'vo_od_6000', 'vo_od_8000'),
            ),
            'classes': ('collapse',)
        }),
        ('Vía Ósea - Oído Izquierdo', {
            'fields': (
                ('vo_oi_250', 'vo_oi_500', 'vo_oi_1000', 'vo_oi_2000'),
                ('vo_oi_3000', 'vo_oi_4000', 'vo_oi_6000', 'vo_oi_8000'),
            ),
            'classes': ('collapse',)
        }),
        ('Campo Electromagnético - VA', {
            'fields': (
                ('va_od_ce_250', 'va_od_ce_500', 'va_od_ce_1000', 'va_od_ce_2000'),
                ('va_od_ce_3000', 'va_od_ce_4000', 'va_od_ce_6000', 'va_od_ce_8000'),
                ('va_oi_ce_250', 'va_oi_ce_500', 'va_oi_ce_1000', 'va_oi_ce_2000'),
                ('va_oi_ce_3000', 'va_oi_ce_4000', 'va_oi_ce_6000', 'va_oi_ce_8000'),
            ),
            'classes': ('collapse',)
        }),
        ('Campo Electromagnético - VO', {
            'fields': (
                ('vo_od_ce_250', 'vo_od_ce_500', 'vo_od_ce_1000', 'vo_od_ce_2000'),
                ('vo_od_ce_3000', 'vo_od_ce_4000', 'vo_od_ce_6000', 'vo_od_ce_8000'),
                ('vo_oi_ce_250', 'vo_oi_ce_500', 'vo_oi_ce_1000', 'vo_oi_ce_2000'),
                ('vo_oi_ce_3000', 'vo_oi_ce_4000', 'vo_oi_ce_6000', 'vo_oi_ce_8000'),
            ),
            'classes': ('collapse',)
        }),
        ('Clasificación CAOHC', {
            'fields': (
                'severidad_od', 'severidad_oi'
            )
        }),
        ('Información RIPS', {
            'fields': (
                'via_ingreso', 'finalidad_consulta', 'causa_externa'
            ),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': (
                'observaciones',
            )
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AntecedenteAuditivoInline,
        AntecedenteAuditivoLaboralInline,
        DiagnosticoAuditivoInline,
        RecomendacionAuditivaInline,
    ]


# Registro de modelos relacionados de audiometría

@admin.register(AntecedenteAuditivo)
class AntecedenteAuditivoAdmin(admin.ModelAdmin):
    list_display = ['audiometria', 'tipo_antecedente', 'observacion']
    list_filter = ['tipo_antecedente']
    search_fields = ['audiometria__ficha_clinica__nombre_trabajador', 'observacion']


@admin.register(AntecedenteAuditivoLaboral)
class AntecedenteAuditivoLaboralAdmin(admin.ModelAdmin):
    list_display = ['audiometria', 'empresa', 'cargo', 'tipo_proteccion', 'tiempo_exposicion_anos']
    list_filter = ['tipo_proteccion', 'tolerancia_proteccion']
    search_fields = ['audiometria__ficha_clinica__nombre_trabajador', 'empresa', 'cargo']


@admin.register(DiagnosticoAuditivo)
class DiagnosticoAuditivoAdmin(admin.ModelAdmin):
    list_display = ['audiometria', 'tipo_diagnostico', 'codigo_cie10', 'nombre_diagnostico', 'lateralidad']
    list_filter = ['tipo_diagnostico', 'lateralidad', 'tipo_impresion']
    search_fields = ['codigo_cie10', 'nombre_diagnostico', 'audiometria__ficha_clinica__nombre_trabajador']


@admin.register(RecomendacionAuditiva)
class RecomendacionAuditivaAdmin(admin.ModelAdmin):
    list_display = ['audiometria', 'codigo', 'seleccionado']
    list_filter = ['codigo', 'seleccionado']
    search_fields = ['audiometria__ficha_clinica__nombre_trabajador']


# ===== ESPIROMETRÍA =====

class RecomendacionEspirometriaInline(admin.TabularInline):
    model = RecomendacionEspirometria
    extra = 0


@admin.register(Espirometria)
class EspirometriaAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'patron_funcional', 'severidad', 'imc', 'created_at'
    ]
    list_filter = [
        'patron_funcional', 'severidad', 'escala_interpretacion',
        'fuma_tabaco', 'es_exfumador', 'asma', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'marca_espirometro', 'observaciones'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'producto', 'peso_kg', 'talla_cm', 'imc',
                'fecha_ingreso_empresa', 'antiguedad_cargo_anos', 'antiguedad_cargo_meses'
            )
        }),
        ('Cargo y Funciones', {
            'fields': (
                'funciones_cargo', 'eps', 'fecha_ultimo_examen', 'resultado_anterior'
            )
        }),
        ('Exposición Ocupacional', {
            'fields': (
                'caracteristica_exposicion', 'riesgos_ocupacionales'
            )
        }),
        ('Elementos de Protección Personal', {
            'fields': (
                'uso_mascarilla', 'uso_respirador', 'uso_otros_epp', 'otros_epp_cual'
            )
        }),
        ('Factores de Riesgo', {
            'fields': (
                'factor_polvo', 'factor_humos', 'factor_gases', 'factor_vapores', 'factor_neblinas',
                'tiempo_exposicion_anos', 'tiempo_exposicion_meses'
            )
        }),
        ('Hábitos Personales', {
            'fields': (
                'fuma_tabaco', 'fuma_cantidad', 'fuma_tiempo',
                'es_exfumador', 'exfumador_cantidad', 'ano_dejo_fumar',
                'practica_deporte', 'deporte_horas_semana', 'deporte_cual',
                'cocina_lena', 'lena_tiempo_exposicion'
            )
        }),
        ('Sintomatología', {
            'fields': (
                'dificultad_respirar', 'dificultad_esfuerzo_fisico',
                'tos_frecuente', 'tos_con_esputo',
                'enfermedad_cardiaca', 'enfermedad_cardiaca_cual',
                'dolor_respirar', 'dolor_respirar_donde',
                'alergia_respiratoria', 'alergia_respiratoria_que',
                'asma', 'asma_edad_ultima_crisis',
                'otra_enfermedad_respiratoria', 'otra_enfermedad_cual'
            ),
            'classes': ('collapse',)
        }),
        ('Valores Espirométricos - CVF', {
            'fields': (
                ('cvf_pre', 'cvf_post', 'cvf_teor'),
                'cvf_observaciones'
            )
        }),
        ('Valores Espirométricos - VEF1', {
            'fields': (
                ('vef1_pre', 'vef1_post', 'vef1_teor'),
                'vef1_observaciones'
            )
        }),
        ('Valores Espirométricos - VEF1/CVF', {
            'fields': (
                ('vef1_cvf_pre', 'vef1_cvf_post', 'vef1_cvf_teor'),
                'vef1_cvf_observaciones'
            )
        }),
        ('Valores Espirométricos - FEF 25-75', {
            'fields': (
                ('fef_25_75_pre', 'fef_25_75_post', 'fef_25_75_teor'),
                'fef_25_75_observaciones'
            )
        }),
        ('Interpretación', {
            'fields': (
                'marca_espirometro', 'fecha_ultima_calibracion', 'escala_interpretacion',
                'patron_funcional', 'severidad'
            )
        }),
        ('Observaciones y Archivos', {
            'fields': (
                'observaciones', 'resultado_archivo'
            )
        }),
        ('Información RIPS', {
            'fields': (
                'via_ingreso', 'finalidad_consulta', 'causa_externa'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        RecomendacionEspirometriaInline,
    ]
    
    def get_imc_display(self, obj):
        if obj.imc:
            if obj.imc < 18.5:
                status = "Bajo peso"
                color = "#17a2b8"
            elif obj.imc < 25:
                status = "Normal"
                color = "#28a745"
            elif obj.imc < 30:
                status = "Sobrepeso"
                color = "#ffc107"
            else:
                status = "Obesidad"
                color = "#dc3545"
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} ({})</span>',
                color, obj.imc, status
            )
        return "No calculado"
    
    get_imc_display.short_description = 'IMC'
    
    def get_patron_display(self, obj):
        colors = {
            'NORMAL': '#28a745',
            'OBSTRUCTIVO': '#ffc107', 
            'RESTRICTIVO': '#dc3545',
            'MIXTO': '#6f42c1'
        }
        color = colors.get(obj.patron_funcional, '#6c757d')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_patron_funcional_display() if obj.patron_funcional else 'No determinado'
        )
    
    get_patron_display.short_description = 'Patrón Funcional'


@admin.register(RecomendacionEspirometria)
class RecomendacionEspirometriaAdmin(admin.ModelAdmin):
    list_display = ['espirometria', 'tipo', 'recomendacion', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['espirometria__ficha_clinica__nombre_trabajador', 'recomendacion']
    date_hierarchy = 'fecha'


# ===== EVALUACIÓN OSTEOMUSCULAR =====

class RecomendacionOsteomuscularInline(admin.TabularInline):
    model = RecomendacionOsteomuscular
    extra = 0


@admin.register(EvaluacionOsteomuscular)
class EvaluacionOsteomuscularAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'get_alteraciones_posturales_total', 
        'get_pruebas_positivas_count', 'imc', 'created_at'
    ]
    list_filter = [
        'extensibilidad', 'flexibilidad_columna', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'observaciones'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'producto', 'peso_kg', 'talla_cm', 'imc', 'funciones_cargo'
            )
        }),
        ('Evaluación Postural', {
            'fields': (
                'evaluacion_postural_observaciones',
                'postura_anterior', 'postura_posterior', 
                'postura_lateral_izq', 'postura_lateral_der'
            ),
            'classes': ('collapse',)
        }),
        ('Movilidad Articular', {
            'fields': (
                'longitud_real', 'longitud_aparente'
            )
        }),
        ('Flexibilidad', {
            'fields': (
                ('extensibilidad', 'extensibilidad_observaciones'),
                ('flexibilidad_columna', 'flexibilidad_columna_observaciones'),
                ('flexibilidad_hombros_izq', 'flexibilidad_hombros_der', 'flexibilidad_hombros_observaciones'),
                ('aductores_izq', 'aductores_der', 'aductores_observaciones'),
                ('gastrocnemios_izq', 'gastrocnemios_der', 'gastrocnemios_observaciones'),
                ('isquiotibiales_izq', 'isquiotibiales_der', 'isquiotibiales_observaciones'),
            )
        }),
        ('Pruebas Semiológicas', {
            'fields': (
                ('bostezo_medial_izq', 'bostezo_medial_der'),
                ('bostezo_lateral_izq', 'bostezo_lateral_der'),
                ('cajon_anterior_izq', 'cajon_anterior_der'),
                ('cajon_posterior_izq', 'cajon_posterior_der'),
                ('thomas_izq', 'thomas_der'),
                ('ober_izq', 'ober_der'),
                ('ely_izq', 'ely_der'),
                ('lasegue_izq', 'lasegue_der'),
            ),
            'classes': ('collapse',)
        }),
        ('Análisis de Marcha - Fase Apoyo', {
            'fields': (
                ('choque_talon_izq', 'choque_talon_der'),
                ('apoyo_plantar_izq', 'apoyo_plantar_der'),
                ('apoyo_medio_izq', 'apoyo_medio_der'),
                ('empuje_izq', 'empuje_der'),
            ),
            'classes': ('collapse',)
        }),
        ('Análisis de Marcha - Fase Balanceo', {
            'fields': (
                ('aceleracion_izq', 'aceleracion_der'),
                ('balanceo_medio_izq', 'balanceo_medio_der'),
                ('desaceleracion_izq', 'desaceleracion_der'),
            ),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': (
                'observaciones',
            )
        }),
        ('Información RIPS', {
            'fields': (
                'via_ingreso', 'finalidad_consulta', 'causa_externa'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        RecomendacionOsteomuscularInline,
    ]
    
    def get_alteraciones_posturales_total(self, obj):
        total = obj.get_alteraciones_posturales_total()
        if total > 0:
            color = "#dc3545" if total > 3 else "#ffc107"
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} alteraciones</span>',
                color, total
            )
        return format_html('<span style="color: #28a745;">Sin alteraciones</span>')
    
    get_alteraciones_posturales_total.short_description = 'Alteraciones Posturales'
    
    def get_pruebas_positivas_count(self, obj):
        pruebas_positivas = obj.get_pruebas_positivas()
        count = len(pruebas_positivas)
        if count > 0:
            color = "#dc3545" if count > 2 else "#ffc107"
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} positivas</span>',
                color, count
            )
        return format_html('<span style="color: #28a745;">Todas negativas</span>')
    
    get_pruebas_positivas_count.short_description = 'Pruebas Semiológicas'
    
    def get_imc_display(self, obj):
        if obj.imc:
            if obj.imc < 18.5:
                status = "Bajo peso"
                color = "#17a2b8"
            elif obj.imc < 25:
                status = "Normal"
                color = "#28a745"
            elif obj.imc < 30:
                status = "Sobrepeso"
                color = "#ffc107"
            else:
                status = "Obesidad"
                color = "#dc3545"
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} ({})</span>',
                color, obj.imc, status
            )
        return "No calculado"
    
    get_imc_display.short_description = 'IMC'


@admin.register(RecomendacionOsteomuscular)
class RecomendacionOsteomuscularAdmin(admin.ModelAdmin):
    list_display = ['evaluacion_osteomuscular', 'tipo', 'recomendacion', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['evaluacion_osteomuscular__ficha_clinica__nombre_trabajador', 'recomendacion']
    date_hierarchy = 'fecha'


# ===== HISTORIA CLÍNICA GENERAL =====

class AntecedenteFamiliarGeneralInline(admin.TabularInline):
    model = AntecedenteFamiliarGeneral
    extra = 0


class AntecedentePersonalGeneralInline(admin.TabularInline):
    model = AntecedentePersonalGeneral
    extra = 0


class DocumentoClinicoInline(admin.TabularInline):
    model = DocumentoClinico
    extra = 0


class DiagnosticoGeneralInline(admin.TabularInline):
    model = DiagnosticoGeneral
    extra = 0


class OrdenMedicamentoInline(admin.TabularInline):
    model = OrdenMedicamento
    extra = 0


class OrdenServicioGeneralInline(admin.TabularInline):
    model = OrdenServicioGeneral
    extra = 0


class OrdenRemisionInline(admin.TabularInline):
    model = OrdenRemision
    extra = 0


class OrdenIncapacidadInline(admin.TabularInline):
    model = OrdenIncapacidad
    extra = 0


class CertificadoMedicoInline(admin.TabularInline):
    model = CertificadoMedico
    extra = 0


class EvolucionGeneralInline(admin.TabularInline):
    model = EvolucionGeneral
    extra = 0


@admin.register(HistoriaClinicaGeneral)
class HistoriaClinicaGeneralAdmin(admin.ModelAdmin):
    list_display = [
        'ficha_clinica', 'tipo_evaluacion_medica', 'get_imc_display', 
        'get_clasificacion_ta_display', 'created_at'
    ]
    list_filter = [
        'tipo_evaluacion_medica', 'estado_civil', 'nivel_educativo',
        'lateralidad_dominante', 'clasificacion_ta', 'created_at'
    ]
    search_fields = [
        'ficha_clinica__nombre_trabajador', 'ficha_clinica__numero_identificacion',
        'motivo_consulta', 'enfermedad_actual', 'observaciones_paraclinicos'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'ficha_clinica', 'tipo_evaluacion_medica', 'estado_civil', 'nivel_educativo',
                'eps', 'afp', 'arl', 'funciones_cargo'
            )
        }),
        ('Motivo de Consulta', {
            'fields': (
                'motivo_consulta', 'enfermedad_actual'
            )
        }),
        ('Signos Vitales', {
            'fields': (
                ('tension_sistolica', 'tension_diastolica', 'clasificacion_ta'),
                ('frecuencia_cardiaca', 'frecuencia_respiratoria', 'pulsioximetria'),
                ('temperatura', 'lateralidad_dominante')
            )
        }),
        ('Antropometría', {
            'fields': (
                ('peso_kg', 'talla_cm', 'imc'),
                ('perimetro_abdominal', 'interpretacion_perimetro')
            )
        }),
        ('Revisión por Sistemas', {
            'fields': (
                'revision_sistemas',
            ),
            'classes': ('collapse',)
        }),
        ('Examen Físico', {
            'fields': (
                'examen_fisico',
            ),
            'classes': ('collapse',)
        }),
        ('Paraclínicos', {
            'fields': (
                'observaciones_paraclinicos',
            )
        }),
        ('Información RIPS', {
            'fields': (
                'via_ingreso', 'finalidad_consulta', 'causa_externa'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AntecedenteFamiliarGeneralInline,
        AntecedentePersonalGeneralInline,
        DocumentoClinicoInline,
        DiagnosticoGeneralInline,
        OrdenMedicamentoInline,
        OrdenServicioGeneralInline,
        OrdenRemisionInline,
        OrdenIncapacidadInline,
        CertificadoMedicoInline,
        EvolucionGeneralInline,
    ]
    
    def get_imc_display(self, obj):
        if obj.imc:
            if obj.imc < 18.5:
                status = "Bajo peso"
                color = "#17a2b8"
            elif obj.imc < 25:
                status = "Normal"
                color = "#28a745"
            elif obj.imc < 30:
                status = "Sobrepeso"
                color = "#ffc107"
            else:
                status = "Obesidad"
                color = "#dc3545"
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} ({})</span>',
                color, obj.imc, status
            )
        return "No calculado"
    
    get_imc_display.short_description = 'IMC'
    
    def get_clasificacion_ta_display(self, obj):
        if obj.clasificacion_ta:
            colors = {
                'NORMAL': '#28a745',
                'PREHIPERTENSION': '#ffc107',
                'HTA_GRADO_1': '#fd7e14',
                'HTA_GRADO_2': '#dc3545',
                'CRISIS_HIPERTENSIVA': '#6f42c1'
            }
            color = colors.get(obj.clasificacion_ta, '#6c757d')
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}/{} - {}</span>',
                color, obj.tension_sistolica or '?', obj.tension_diastolica or '?',
                obj.get_clasificacion_ta_display()
            )
        return "No evaluada"
    
    get_clasificacion_ta_display.short_description = 'Tensión Arterial'


@admin.register(AntecedenteFamiliarGeneral)
class AntecedenteFamiliarGeneralAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'tipo_antecedente', 'observacion', 'fecha']
    list_filter = ['tipo_antecedente', 'fecha']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'observacion']
    date_hierarchy = 'fecha'


@admin.register(AntecedentePersonalGeneral)
class AntecedentePersonalGeneralAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'tipo_antecedente', 'observacion', 'fecha']
    list_filter = ['tipo_antecedente', 'fecha']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'observacion']
    date_hierarchy = 'fecha'


@admin.register(DocumentoClinico)
class DocumentoClinicoAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'nombre_documento', 'usuario_creacion', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'nombre_documento', 'observaciones']
    date_hierarchy = 'fecha_creacion'


@admin.register(DiagnosticoGeneral)
class DiagnosticoGeneralAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'tipo_diagnostico', 'codigo_cie10', 'nombre_diagnostico', 'fecha']
    list_filter = ['tipo_diagnostico', 'tipo_impresion', 'fecha']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'codigo_cie10', 'nombre_diagnostico']
    date_hierarchy = 'fecha'


@admin.register(OrdenMedicamento)
class OrdenMedicamentoAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'numero_orden', 'nombre_medicamento', 'cantidad', 'posologia', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'nombre_medicamento']
    date_hierarchy = 'fecha_creacion'


@admin.register(OrdenServicioGeneral)
class OrdenServicioGeneralAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'numero_orden', 'nombre_servicio', 'cantidad', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'nombre_servicio']
    date_hierarchy = 'fecha_creacion'


@admin.register(OrdenRemision)
class OrdenRemisionAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'numero_orden', 'nombre_especialidad', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'nombre_especialidad', 'motivo_remision']
    date_hierarchy = 'fecha_creacion'


@admin.register(OrdenIncapacidad)
class OrdenIncapacidadAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'numero_orden', 'tipo', 'dias', 'fecha_creacion']
    list_filter = ['tipo', 'fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'motivo_incapacidad']
    date_hierarchy = 'fecha_creacion'


@admin.register(CertificadoMedico)
class CertificadoMedicoAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'numero_certificado', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'descripcion_certificado']
    date_hierarchy = 'fecha_creacion'


@admin.register(EvolucionGeneral)
class EvolucionGeneralAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'profesional_asistencial', 'fecha']
    list_filter = ['profesional_asistencial', 'fecha']
    search_fields = ['historia_clinica__ficha_clinica__nombre_trabajador', 'evolucion']
    date_hierarchy = 'fecha'


# Configuración del sitio admin
admin.site.site_header = "Admisión - Recepción"
admin.site.site_title = "Admisión - Recepción Admin"
admin.site.index_title = "Administración de Admisión - Recepción"