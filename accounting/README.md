# 📊 Módulo de Contabilidad - HMetaHIS

## Descripción
El módulo de contabilidad proporciona una gestión integral de la contabilidad hospitalaria, incluyendo plan de cuentas, asientos contables, terceros, períodos contables y reportes financieros.

## 🏗️ Estructura del Módulo

### Modelos Principales

#### 1. **PeriodoContable**
- Gestión de períodos contables
- Control de apertura y cierre de períodos
- Validación de fechas

#### 2. **CuentaContable**
- Plan de cuentas contables (PUC)
- Estructura jerárquica con cuentas padre/hijo
- Tipos: Activo, Pasivo, Patrimonio, Ingreso, Gasto, Orden
- Control de activación/desactivación

#### 3. **Tercero**
- Gestión de proveedores, clientes y otros terceros
- Tipos: Persona Natural y Jurídica
- Información completa de contacto

#### 4. **Diario**
- Diarios contables (General, Caja, Banco, Ventas, Compras)
- Control de activación

#### 5. **Impuesto**
- Configuración de impuestos (IVA, ICA, Retenciones)
- Porcentajes y tipos configurables

#### 6. **AsientoContable**
- Asientos contables principales
- Relación con diarios, períodos y terceros
- Control de creación y auditoría

#### 7. **LineaAsiento**
- Líneas individuales de cada asiento
- Validación de débito/crédito
- Relación con cuentas, impuestos y terceros

#### 8. **DatosEmpresa**
- Información básica de la empresa
- Datos del representante legal
- Información de contacto completa

#### 9. **CentroCosto**
- Centros de costos para contratos y convenios
- Control de fechas de vigencia
- Gestión de contratos específicos

#### 10. **ComprobanteContable**
- Comprobantes contables con tipos específicos
- Estados: Activo, Anulado, Sin Procesar
- Numeración automática según formato
- Tipos: FC, CE, FVE, CI

#### 11. **CertificadoRetencion**
- Certificados de retención en la fuente
- Cálculo automático de valores retenidos
- Tipos: Renta, ICA, IVA, Otro
- Generación de reportes PDF

## 🚀 Funcionalidades

### Dashboard Principal
- Vista general de estadísticas contables
- Acceso rápido a todas las funcionalidades
- Contadores de elementos principales

### Gestión de Asientos
- Creación y edición de asientos contables
- Formset dinámico para líneas de asiento
- Validación automática de balance
- Control de usuario que crea el asiento

### Plan de Cuentas
- Gestión jerárquica del PUC
- Códigos únicos por cuenta
- Control de activación/desactivación
- Estructura padre/hijo

### Terceros
- Gestión completa de proveedores y clientes
- Información de contacto detallada
- Control de activación

### Reportes Financieros
- **Balance General**: Activos, pasivos y patrimonio
- **Estado de Resultados**: Ingresos, gastos y resultado neto
- **Libro Diario**: Movimientos detallados
- **Estado de Flujo de Efectivo**: Actividades operacionales, inversión y financiación
- **Análisis Presupuestal**: Comparación presupuesto vs real con análisis de variaciones
- **Análisis de Costos**: Costos directos e indirectos por centro de costo
- **Reportes Fiscales**: IVA, retenciones, ICA y obligaciones fiscales
- **Análisis de Cartera**: Cuentas por cobrar y pagar con envejecimiento
- **Indicadores Financieros**: Ratios de liquidez, solvencia, rentabilidad y eficiencia
- **Reportes de Auditoría**: Trail de auditoría y cambios en registros
- **Reporte Bancario**: Movimientos bancarios y saldos
- **Conciliación Bancaria**: Conciliación de movimientos bancarios
- **Filtros por período, fecha, tipo de reporte y banco**

### Configuración
- Períodos contables
- Diarios contables
- Impuestos
- Parámetros del sistema

### Comprobantes Contables
- **Factura de Compra (FC)**: Para causar gastos
- **Comprobante de Egreso (CE)**: Para pagar gastos
- **Factura Electrónica (FVE)**: Para causar ingresos
- **Comprobante de Ingreso (CI)**: Para registrar pagos recibidos
- Estados: Activo, Anulado, Sin Procesar
- Numeración automática con formato AAAA-MM-DD-NNNN

### Certificados de Retención
- Generación automática de certificados
- Cálculo de valores retenidos
- Tipos: Renta, ICA, IVA, Otro
- Exportación a PDF

### Centros de Costo
- Gestión de contratos y convenios
- Control de fechas de vigencia
- Asociación con comprobantes y asientos

## 📋 URLs Disponibles

### Dashboard y Reportes
- `/accounting/` - Dashboard principal
- `/accounting/reportes/` - Reportes financieros

### Gestión de Asientos
- `/accounting/asientos/` - Lista de asientos
- `/accounting/asientos/crear/` - Crear asiento
- `/accounting/asientos/<id>/` - Ver asiento
- `/accounting/asientos/<id>/editar/` - Editar asiento
- `/accounting/asientos/<id>/eliminar/` - Eliminar asiento

### Plan de Cuentas
- `/accounting/cuentas/` - Lista de cuentas
- `/accounting/cuentas/crear/` - Crear cuenta
- `/accounting/cuentas/<id>/` - Ver cuenta
- `/accounting/cuentas/<id>/editar/` - Editar cuenta
- `/accounting/cuentas/<id>/eliminar/` - Eliminar cuenta

### Terceros
- `/accounting/terceros/` - Lista de terceros
- `/accounting/terceros/crear/` - Crear tercero
- `/accounting/terceros/<id>/` - Ver tercero
- `/accounting/terceros/<id>/editar/` - Editar tercero
- `/accounting/terceros/<id>/eliminar/` - Eliminar tercero

### Configuración
- `/accounting/periodos/` - Períodos contables
- `/accounting/diarios/` - Diarios contables
- `/accounting/impuestos/` - Impuestos

### Datos de Empresa
- `/accounting/empresa/` - Datos de la empresa
- `/accounting/empresa/crear/` - Crear datos de empresa
- `/accounting/empresa/<id>/` - Ver datos de empresa
- `/accounting/empresa/<id>/editar/` - Editar datos de empresa
- `/accounting/empresa/<id>/eliminar/` - Eliminar datos de empresa

### Centros de Costo
- `/accounting/centros-costo/` - Centros de costo
- `/accounting/centros-costo/crear/` - Crear centro de costo
- `/accounting/centros-costo/<id>/` - Ver centro de costo
- `/accounting/centros-costo/<id>/editar/` - Editar centro de costo
- `/accounting/centros-costo/<id>/eliminar/` - Eliminar centro de costo

### Comprobantes Contables
- `/accounting/comprobantes/` - Comprobantes contables
- `/accounting/comprobantes/crear/` - Crear comprobante
- `/accounting/comprobantes/<id>/` - Ver comprobante
- `/accounting/comprobantes/<id>/editar/` - Editar comprobante
- `/accounting/comprobantes/<id>/eliminar/` - Eliminar comprobante

### Certificados de Retención
- `/accounting/certificados/` - Certificados de retención
- `/accounting/certificados/crear/` - Crear certificado
- `/accounting/certificados/<id>/` - Ver certificado
- `/accounting/certificados/<id>/editar/` - Editar certificado
- `/accounting/certificados/<id>/eliminar/` - Eliminar certificado

## 🔧 Utilidades y Funciones

### Funciones Principales
- `calcular_saldo_cuenta()` - Calcula saldo de una cuenta
- `generar_balance_general()` - Genera balance general
- `generar_estado_resultados()` - Genera estado de resultados
- `validar_asiento_balanceado()` - Valida balance de asiento
- `obtener_mayor_cuenta()` - Genera mayor de cuenta
- `crear_asiento_automatico()` - Crea asiento automático

### Señales Automáticas
- Validación de balance en asientos
- Actualización de códigos de subcuentas
- Validación de líneas de asiento

## 🎨 Templates

### Templates Principales
- `dashboard.html` - Dashboard principal
- `reportes.html` - Reportes financieros
- `asientocontable_form.html` - Formulario de asientos con formset
- `asientocontable_list.html` - Lista de asientos
- `asientocontable_detail.html` - Detalle de asiento

### Templates de Gestión
- Templates CRUD para todos los modelos
- Formularios con validación
- Listas con paginación
- Detalles con información completa

## 🔒 Validaciones

### Asientos Contables
- Balance automático (débito = crédito)
- Validación de fechas dentro del período
- Control de usuario que crea el asiento

### Líneas de Asiento
- Una línea no puede tener débito y crédito simultáneamente
- Una línea debe tener débito o crédito
- Validación de cuentas activas

### Plan de Cuentas
- Códigos únicos
- Estructura jerárquica válida
- Control de activación

## 📊 Reportes Disponibles

### Reportes Básicos
- **Balance General**: Activos corrientes y no corrientes, pasivos y patrimonio
- **Estado de Resultados**: Ingresos operacionales, gastos y resultado neto
- **Libro Diario**: Movimientos cronológicos con filtros por fecha y período
- **Reporte Bancario**: Movimientos bancarios y saldos por banco
- **Conciliación Bancaria**: Conciliación de movimientos con análisis de diferencias

### Reportes Avanzados
- **Estado de Flujo de Efectivo**: Actividades operacionales, inversión y financiación
- **Análisis Presupuestal**: Comparación presupuesto vs real con análisis de variaciones
- **Análisis de Costos**: Costos directos e indirectos por centro de costo
- **Reportes Fiscales**: IVA, retenciones, ICA y obligaciones fiscales
- **Análisis de Cartera**: Cuentas por cobrar y pagar con envejecimiento
- **Indicadores Financieros**: Ratios de liquidez, solvencia, rentabilidad y eficiencia
- **Reportes de Auditoría**: Trail de auditoría y cambios en registros

### Estadísticas
- Total de asientos
- Total de débitos y créditos
- Balance general
- Contadores por tipo

## 🚀 Instalación y Configuración

1. **Agregar a INSTALLED_APPS**:
```python
INSTALLED_APPS = [
    ...
    'accounting',
    ...
]
```

2. **Ejecutar migraciones**:
```bash
python manage.py makemigrations accounting
python manage.py migrate
```

3. **Configurar URLs**:
```python
urlpatterns = [
    ...
    path('accounting/', include('accounting.urls')),
    ...
]
```

## 🔧 Personalización

### Agregar Nuevos Tipos de Cuenta
Modificar las opciones en el modelo `CuentaContable`:
```python
tipo = models.CharField(max_length=20, choices=[
    ('ACTIVO','Activo'),
    ('PASIVO','Pasivo'),
    ('PATRIMONIO','Patrimonio'),
    ('INGRESO','Ingreso'),
    ('GASTO','Gasto'),
    ('ORDEN','Orden'),
    ('NUEVO_TIPO','Nuevo Tipo'),  # Agregar aquí
])
```

### Agregar Nuevos Tipos de Diario
Modificar las opciones en el modelo `Diario`:
```python
tipo = models.CharField(max_length=20, choices=[
    ('GENERAL','General'),
    ('CAJA','Caja'),
    ('BANCO','Banco'),
    ('VENTAS','Ventas'),
    ('COMPRAS','Compras'),
    ('NUEVO_DIARIO','Nuevo Diario'),  # Agregar aquí
])
```

## 📈 Próximas Mejoras

- [ ] Exportación a Excel/PDF
- [ ] Integración con módulo de facturación
- [ ] Conciliación bancaria
- [ ] Presupuestos
- [ ] Análisis de costos por departamento
- [ ] Dashboard con gráficos
- [ ] API REST para integraciones
- [ ] Auditoría completa de cambios

## 🤝 Contribución

Para contribuir al módulo de contabilidad:

1. Crear una rama para tu feature
2. Implementar las mejoras
3. Agregar tests
4. Documentar cambios
5. Crear pull request

## 📞 Soporte

Para soporte técnico o consultas sobre el módulo de contabilidad, contactar al equipo de desarrollo de HMetaHIS. 

## 🆕 Nuevas Funcionalidades Agregadas

### 12. **MovimientoBancario**
- Gestión de movimientos bancarios
- Conciliación automática con asientos contables
- Control de estados (conciliado/pendiente)
- Filtros por banco, tipo y fecha
- Integración con reportes bancarios

### 13. **CierreContable**
- Cierre de períodos contables
- Control de asientos de cierre
- Auditoría de cierres realizados
- Validación de períodos cerrados
- Reportes de cierre

### 14. **AuditLog**
- Log de auditoría para cambios en registros
- Seguimiento de acciones (crear, actualizar, eliminar)
- Almacenamiento de datos anteriores y nuevos
- Control de IP y usuario
- Reportes de auditoría

### 15. **Presupuesto**
- Gestión de presupuestos por cuenta y centro de costo
- Cálculo automático de variaciones
- Comparación presupuesto vs real
- Alertas de desviaciones
- Reportes de presupuestos

## 🔄 Integración con Otros Módulos

### Compras → Contabilidad
- Integración automática de facturas de proveedores
- Generación de asientos contables automáticos
- Control de cuentas por pagar

### Ventas → Contabilidad
- Integración de facturación a pacientes
- Generación de asientos de ingresos
- Control de cuentas por cobrar

### RRHH → Contabilidad
- Integración de nómina y prestaciones
- Asientos automáticos de gastos de personal
- Control de retenciones

### Inventarios → Contabilidad
- Valorización de inventarios
- Ajustes de inventario automáticos
- Control de costos

## 📊 Reportes Avanzados

### Estados Financieros
- **Balance General**: Activos, pasivos y patrimonio
- **Estado de Resultados**: Ingresos, gastos y resultado neto
- **Flujo de Caja**: Movimientos de efectivo
- **Aged Trial Balance**: Envejecimiento de cuentas

### Reportes de Gestión
- **Conciliación Bancaria**: Estado de cuentas bancarias
- **Presupuestos vs Real**: Análisis de desviaciones
- **Ratios Financieros**: Indicadores de rentabilidad
- **Auditoría**: Trail de cambios en registros

### Reportes Fiscales
- **Declaración de IVA**: Reportes para SAT
- **Retenciones**: Certificados de retención
- **ICA**: Impuesto de industria y comercio

## 🚀 Próximas Funcionalidades

### Análisis Financiero Avanzado
- Ratios financieros automáticos
- Análisis de tendencias
- Indicadores de rentabilidad
- Comparación de períodos

### Integración con APIs
- Conexión con bancos para movimientos automáticos
- Integración con sistemas de facturación electrónica
- APIs para reportes externos

### Automatización
- Cierres automáticos de períodos
- Conciliación automática bancaria
- Alertas de desviaciones presupuestales
- Notificaciones de vencimientos

## 📋 Checklist de Implementación

- [x] Modelos de datos básicos
- [x] CRUD completo para todos los modelos
- [x] Dashboard con estadísticas
- [x] Reportes financieros básicos
- [x] Validaciones de balance
- [x] Numeración automática
- [x] Conciliación bancaria
- [x] Cierre contable
- [x] Auditoría de cambios
- [x] Gestión de presupuestos
- [ ] Integración automática con otros módulos
- [ ] Reportes fiscales avanzados
- [ ] Análisis financiero automático
- [ ] APIs para integración externa 