from decimal import Decimal
from django.db.models import Sum, Q
from .models import CuentaContable, LineaAsiento, AsientoContable

def calcular_saldo_cuenta(cuenta, fecha_inicio=None, fecha_fin=None):
    """
    Calcula el saldo de una cuenta contable en un período específico
    """
    lineas = LineaAsiento.objects.filter(cuenta=cuenta)
    
    if fecha_inicio:
        lineas = lineas.filter(asiento__fecha__gte=fecha_inicio)
    
    if fecha_fin:
        lineas = lineas.filter(asiento__fecha__lte=fecha_fin)
    
    total_debito = lineas.aggregate(total=Sum('debito'))['total'] or Decimal('0.00')
    total_credito = lineas.aggregate(total=Sum('credito'))['total'] or Decimal('0.00')
    
    # Para cuentas de activo y gasto: débito - crédito
    # Para cuentas de pasivo, patrimonio e ingreso: crédito - débito
    if cuenta.tipo in ['ACTIVO', 'GASTO']:
        return total_debito - total_credito
    else:
        return total_credito - total_debito

def generar_balance_general(fecha_corte=None):
    """
    Genera un balance general a una fecha específica
    """
    balance = {
        'activos': [],
        'pasivos': [],
        'patrimonio': []
    }
    
    # Obtener todas las cuentas activas
    cuentas = CuentaContable.objects.filter(activa=True)
    
    for cuenta in cuentas:
        saldo = calcular_saldo_cuenta(cuenta, fecha_fin=fecha_corte)
        
        if saldo != 0:
            item = {
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'saldo': saldo
            }
            
            if cuenta.tipo == 'ACTIVO':
                balance['activos'].append(item)
            elif cuenta.tipo == 'PASIVO':
                balance['pasivos'].append(item)
            elif cuenta.tipo == 'PATRIMONIO':
                balance['patrimonio'].append(item)
    
    return balance

def generar_estado_resultados(fecha_inicio, fecha_fin):
    """
    Genera un estado de resultados para un período específico
    """
    ingresos = []
    gastos = []
    
    # Cuentas de ingreso
    cuentas_ingreso = CuentaContable.objects.filter(tipo='INGRESO', activa=True)
    for cuenta in cuentas_ingreso:
        saldo = calcular_saldo_cuenta(cuenta, fecha_inicio, fecha_fin)
        if saldo != 0:
            ingresos.append({
                'cuenta': cuenta.nombre,
                'monto': saldo
            })
    
    # Cuentas de gasto
    cuentas_gasto = CuentaContable.objects.filter(tipo='GASTO', activa=True)
    for cuenta in cuentas_gasto:
        saldo = calcular_saldo_cuenta(cuenta, fecha_inicio, fecha_fin)
        if saldo != 0:
            gastos.append({
                'cuenta': cuenta.nombre,
                'monto': abs(saldo)
            })
    
    total_ingresos = sum(item['monto'] for item in ingresos)
    total_gastos = sum(item['monto'] for item in gastos)
    resultado_neto = total_ingresos - total_gastos
    
    return {
        'ingresos': ingresos,
        'gastos': gastos,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'resultado_neto': resultado_neto
    }

def validar_asiento_balanceado(asiento):
    """
    Valida que un asiento contable esté balanceado
    """
    lineas = LineaAsiento.objects.filter(asiento=asiento)
    total_debito = lineas.aggregate(total=Sum('debito'))['total'] or Decimal('0.00')
    total_credito = lineas.aggregate(total=Sum('credito'))['total'] or Decimal('0.00')
    
    return abs(total_debito - total_credito) < Decimal('0.01')

def obtener_mayor_cuenta(cuenta, fecha_inicio=None, fecha_fin=None):
    """
    Genera el mayor de una cuenta específica
    """
    lineas = LineaAsiento.objects.filter(cuenta=cuenta)
    
    if fecha_inicio:
        lineas = lineas.filter(asiento__fecha__gte=fecha_inicio)
    
    if fecha_fin:
        lineas = lineas.filter(asiento__fecha__lte=fecha_fin)
    
    lineas = lineas.select_related('asiento').order_by('asiento__fecha', 'asiento__id')
    
    saldo_acumulado = Decimal('0.00')
    mayor = []
    
    for linea in lineas:
        if cuenta.tipo in ['ACTIVO', 'GASTO']:
            saldo_acumulado += linea.debito - linea.credito
        else:
            saldo_acumulado += linea.credito - linea.debito
        
        mayor.append({
            'fecha': linea.asiento.fecha,
            'asiento': linea.asiento.id,
            'descripcion': linea.descripcion or linea.asiento.descripcion,
            'debito': linea.debito,
            'credito': linea.credito,
            'saldo': saldo_acumulado
        })
    
    return mayor

def crear_asiento_automatico(descripcion, lineas_data, diario, periodo, tercero=None, referencia=None):
    """
    Crea un asiento contable automáticamente con validaciones
    """
    from django.contrib.auth.models import User
    
    # Validar que las líneas estén balanceadas
    total_debito = sum(linea['debito'] for linea in lineas_data)
    total_credito = sum(linea['credito'] for linea in lineas_data)
    
    if abs(total_debito - total_credito) > Decimal('0.01'):
        raise ValueError("El asiento no está balanceado")
    
    # Crear el asiento
    asiento = AsientoContable.objects.create(
        descripcion=descripcion,
        diario=diario,
        periodo=periodo,
        tercero=tercero,
        referencia=referencia
    )
    
    # Crear las líneas
    for linea_data in lineas_data:
        LineaAsiento.objects.create(
            asiento=asiento,
            cuenta=linea_data['cuenta'],
            descripcion=linea_data.get('descripcion', ''),
            debito=linea_data['debito'],
            credito=linea_data['credito'],
            impuesto=linea_data.get('impuesto'),
            tercero=linea_data.get('tercero')
        )
    
    return asiento 