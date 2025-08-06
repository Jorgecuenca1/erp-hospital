#!/usr/bin/env python
"""
Script para crear datos de ejemplo en el módulo de contabilidad
"""
import os
import sys
import django
from datetime import date, datetime
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from accounting.models import (
    DatosEmpresa, CentroCosto, PeriodoContable, CuentaContable, 
    Tercero, Diario, Impuesto, ComprobanteContable, AsientoContable,
    LineaAsiento, CertificadoRetencion
)

def crear_datos_ejemplo():
    print("🏥 Creando datos de ejemplo para el módulo de contabilidad...")
    
    # Obtener usuario admin
    usuario = User.objects.get(username='jorge')
    
    # 1. Crear Datos de Empresa
    print("📋 Creando datos de empresa...")
    empresa, created = DatosEmpresa.objects.get_or_create(
        nit='900123456-7',
        defaults={
            'nombre': 'Hospital San Jorge S.A.S.',
            'direccion': 'Calle 123 #45-67, Bogotá',
            'telefono': '(57) 1 2345678',
            'email': 'contacto@hospitalsanjorge.com',
            'ciudad': 'Bogotá D.C.',
            'representante_legal': 'Dr. Jorge Pérez',
            'cargo_representante': 'Director General'
        }
    )
    print(f"✅ Empresa creada: {empresa.nombre}")
    
    # 2. Crear Centros de Costo
    print("🏢 Creando centros de costo...")
    centros_costo = [
        {
            'codigo': 'CC001',
            'nombre': 'Urgencias',
            'descripcion': 'Centro de costos para servicios de urgencias',
            'contrato': 'CON-2024-001',
            'fecha_inicio': date(2024, 1, 1),
            'fecha_fin': date(2024, 12, 31)
        },
        {
            'codigo': 'CC002',
            'nombre': 'Cirugía',
            'descripcion': 'Centro de costos para servicios quirúrgicos',
            'contrato': 'CON-2024-002',
            'fecha_inicio': date(2024, 1, 1),
            'fecha_fin': date(2024, 12, 31)
        },
        {
            'codigo': 'CC003',
            'nombre': 'Laboratorio',
            'descripcion': 'Centro de costos para servicios de laboratorio',
            'contrato': 'CON-2024-003',
            'fecha_inicio': date(2024, 1, 1),
            'fecha_fin': date(2024, 12, 31)
        }
    ]
    
    for cc_data in centros_costo:
        cc, created = CentroCosto.objects.get_or_create(
            codigo=cc_data['codigo'],
            defaults=cc_data
        )
        print(f"✅ Centro de costo creado: {cc.codigo} - {cc.nombre}")
    
    # 3. Crear Período Contable
    print("📅 Creando período contable...")
    periodo, created = PeriodoContable.objects.get_or_create(
        nombre='2024',
        defaults={
            'fecha_inicio': date(2024, 1, 1),
            'fecha_fin': date(2024, 12, 31),
            'cerrado': False
        }
    )
    print(f"✅ Período contable creado: {periodo.nombre}")
    
    # 4. Crear Plan de Cuentas
    print("📊 Creando plan de cuentas...")
    cuentas_data = [
        # Activos
        {'codigo': '1100', 'nombre': 'Caja y Bancos', 'tipo': 'ACTIVO'},
        {'codigo': '1110', 'nombre': 'Caja General', 'tipo': 'ACTIVO'},
        {'codigo': '1120', 'nombre': 'Bancos', 'tipo': 'ACTIVO'},
        {'codigo': '1300', 'nombre': 'Cuentas por Cobrar', 'tipo': 'ACTIVO'},
        {'codigo': '1310', 'nombre': 'Pacientes', 'tipo': 'ACTIVO'},
        {'codigo': '1320', 'nombre': 'EPS', 'tipo': 'ACTIVO'},
        {'codigo': '1500', 'nombre': 'Propiedades y Equipos', 'tipo': 'ACTIVO'},
        {'codigo': '1510', 'nombre': 'Equipos Médicos', 'tipo': 'ACTIVO'},
        {'codigo': '1520', 'nombre': 'Muebles y Enseres', 'tipo': 'ACTIVO'},
        
        # Pasivos
        {'codigo': '2100', 'nombre': 'Cuentas por Pagar', 'tipo': 'PASIVO'},
        {'codigo': '2110', 'nombre': 'Proveedores', 'tipo': 'PASIVO'},
        {'codigo': '2200', 'nombre': 'Impuestos por Pagar', 'tipo': 'PASIVO'},
        {'codigo': '2210', 'nombre': 'IVA por Pagar', 'tipo': 'PASIVO'},
        {'codigo': '2220', 'nombre': 'ICA por Pagar', 'tipo': 'PASIVO'},
        {'codigo': '2300', 'nombre': 'Retenciones por Pagar', 'tipo': 'PASIVO'},
        
        # Patrimonio
        {'codigo': '3100', 'nombre': 'Capital Social', 'tipo': 'PATRIMONIO'},
        {'codigo': '3200', 'nombre': 'Utilidades Retenidas', 'tipo': 'PATRIMONIO'},
        {'codigo': '3300', 'nombre': 'Utilidad del Ejercicio', 'tipo': 'PATRIMONIO'},
        
        # Ingresos
        {'codigo': '4100', 'nombre': 'Ingresos por Servicios', 'tipo': 'INGRESO'},
        {'codigo': '4110', 'nombre': 'Consultas Médicas', 'tipo': 'INGRESO'},
        {'codigo': '4120', 'nombre': 'Cirugías', 'tipo': 'INGRESO'},
        {'codigo': '4130', 'nombre': 'Laboratorio', 'tipo': 'INGRESO'},
        {'codigo': '4140', 'nombre': 'Radiología', 'tipo': 'INGRESO'},
        
        # Gastos
        {'codigo': '5100', 'nombre': 'Gastos de Personal', 'tipo': 'GASTO'},
        {'codigo': '5110', 'nombre': 'Salarios', 'tipo': 'GASTO'},
        {'codigo': '5120', 'nombre': 'Prestaciones Sociales', 'tipo': 'GASTO'},
        {'codigo': '5200', 'nombre': 'Gastos Administrativos', 'tipo': 'GASTO'},
        {'codigo': '5210', 'nombre': 'Servicios Públicos', 'tipo': 'GASTO'},
        {'codigo': '5220', 'nombre': 'Arriendo', 'tipo': 'GASTO'},
        {'codigo': '5300', 'nombre': 'Gastos de Operación', 'tipo': 'GASTO'},
        {'codigo': '5310', 'nombre': 'Insumos Médicos', 'tipo': 'GASTO'},
        {'codigo': '5320', 'nombre': 'Medicamentos', 'tipo': 'GASTO'},
    ]
    
    for cuenta_data in cuentas_data:
        cuenta, created = CuentaContable.objects.get_or_create(
            codigo=cuenta_data['codigo'],
            defaults=cuenta_data
        )
        print(f"✅ Cuenta creada: {cuenta.codigo} - {cuenta.nombre}")
    
    # 5. Crear Terceros
    print("👥 Creando terceros...")
    terceros_data = [
        {
            'tipo': 'JURIDICA',
            'nombre': 'EPS Sanitas S.A.',
            'nit': '860001234-5',
            'direccion': 'Calle 100 #15-60, Bogotá',
            'telefono': '(57) 1 2345678',
            'email': 'contacto@sanitas.com',
            'ciudad': 'Bogotá D.C.'
        },
        {
            'tipo': 'JURIDICA',
            'nombre': 'Farmacia Central Ltda.',
            'nit': '900123456-8',
            'direccion': 'Carrera 15 #85-20, Bogotá',
            'telefono': '(57) 1 8765432',
            'email': 'ventas@farmaciacentral.com',
            'ciudad': 'Bogotá D.C.'
        },
        {
            'tipo': 'NATURAL',
            'nombre': 'Dr. Carlos Mendoza',
            'nit': '79123456',
            'direccion': 'Calle 72 #10-45, Bogotá',
            'telefono': '(57) 300 1234567',
            'email': 'carlos.mendoza@email.com',
            'ciudad': 'Bogotá D.C.'
        }
    ]
    
    for tercero_data in terceros_data:
        tercero, created = Tercero.objects.get_or_create(
            nit=tercero_data['nit'],
            defaults=tercero_data
        )
        print(f"✅ Tercero creado: {tercero.nombre}")
    
    # 6. Crear Diarios
    print("📝 Creando diarios...")
    diarios_data = [
        {'nombre': 'Diario General', 'codigo': 'DG', 'tipo': 'GENERAL'},
        {'nombre': 'Diario de Caja', 'codigo': 'DC', 'tipo': 'CAJA'},
        {'nombre': 'Diario de Banco', 'codigo': 'DB', 'tipo': 'BANCO'},
        {'nombre': 'Diario de Ventas', 'codigo': 'DV', 'tipo': 'VENTAS'},
        {'nombre': 'Diario de Compras', 'codigo': 'DCMP', 'tipo': 'COMPRAS'},
    ]
    
    for diario_data in diarios_data:
        diario, created = Diario.objects.get_or_create(
            codigo=diario_data['codigo'],
            defaults=diario_data
        )
        print(f"✅ Diario creado: {diario.codigo} - {diario.nombre}")
    
    # 7. Crear Impuestos
    print("💰 Creando impuestos...")
    impuestos_data = [
        {'nombre': 'IVA 19%', 'codigo': 'IVA19', 'porcentaje': 19.00, 'tipo': 'IVA'},
        {'nombre': 'ICA 6.96x1000', 'codigo': 'ICA696', 'porcentaje': 0.696, 'tipo': 'ICA'},
        {'nombre': 'Retención Renta 2.5%', 'codigo': 'RENTA25', 'porcentaje': 2.50, 'tipo': 'RETENCION'},
        {'nombre': 'Retención IVA 15%', 'codigo': 'RIVA15', 'porcentaje': 15.00, 'tipo': 'RETENCION'},
    ]
    
    for impuesto_data in impuestos_data:
        impuesto, created = Impuesto.objects.get_or_create(
            codigo=impuesto_data['codigo'],
            defaults=impuesto_data
        )
        print(f"✅ Impuesto creado: {impuesto.nombre}")
    
    # 8. Crear Comprobantes Contables
    print("🧾 Creando comprobantes contables...")
    eps_sanitas = Tercero.objects.get(nit='860001234-5')
    farmacia_central = Tercero.objects.get(nit='900123456-8')
    dr_carlos = Tercero.objects.get(nit='79123456')
    centro_urgencias = CentroCosto.objects.get(codigo='CC001')
    
    comprobantes_data = [
        {
            'tipo': 'FVE',
            'numero': '202407190001',
            'fecha': date(2024, 7, 19),
            'tercero': eps_sanitas,
            'centro_costo': centro_urgencias,
            'descripcion': 'Factura por servicios de urgencias',
            'valor': Decimal('2500000.00'),
            'estado': 'ACTIVO'
        },
        {
            'tipo': 'FC',
            'numero': '202407190002',
            'fecha': date(2024, 7, 19),
            'tercero': farmacia_central,
            'centro_costo': None,
            'descripcion': 'Compra de medicamentos',
            'valor': Decimal('1500000.00'),
            'estado': 'ACTIVO'
        },
        {
            'tipo': 'CE',
            'numero': '202407190003',
            'fecha': date(2024, 7, 19),
            'tercero': dr_carlos,
            'centro_costo': None,
            'descripcion': 'Pago honorarios médicos',
            'valor': Decimal('800000.00'),
            'estado': 'ACTIVO'
        }
    ]
    
    for comp_data in comprobantes_data:
        comp, created = ComprobanteContable.objects.get_or_create(
            numero=comp_data['numero'],
            defaults=comp_data
        )
        if created:
            comp.creado_por = usuario
            comp.save()
        print(f"✅ Comprobante creado: {comp.tipo}-{comp.numero}")
    
    # 9. Crear Asientos Contables
    print("📊 Creando asientos contables...")
    diario_general = Diario.objects.get(codigo='DG')
    cuenta_ingresos = CuentaContable.objects.get(codigo='4110')
    cuenta_caja = CuentaContable.objects.get(codigo='1110')
    cuenta_proveedores = CuentaContable.objects.get(codigo='2110')
    cuenta_gastos = CuentaContable.objects.get(codigo='5110')
    
    # Asiento 1: Ingreso por servicios
    asiento1 = AsientoContable.objects.create(
        fecha=date(2024, 7, 19),
        descripcion='Registro de ingreso por servicios de urgencias',
        diario=diario_general,
        periodo=periodo,
        tercero=eps_sanitas,
        centro_costo=centro_urgencias,
        comprobante=ComprobanteContable.objects.get(numero='202407190001'),
        creado_por=usuario,
        referencia='AS-001'
    )
    
    # Líneas del asiento 1
    LineaAsiento.objects.create(
        asiento=asiento1,
        cuenta=cuenta_ingresos,
        descripcion='Ingreso por servicios de urgencias',
        debito=Decimal('0.00'),
        credito=Decimal('2500000.00'),
        tercero=eps_sanitas,
        centro_costo=centro_urgencias
    )
    
    LineaAsiento.objects.create(
        asiento=asiento1,
        cuenta=cuenta_caja,
        descripcion='Cobro en efectivo',
        debito=Decimal('2500000.00'),
        credito=Decimal('0.00'),
        tercero=eps_sanitas,
        centro_costo=centro_urgencias
    )
    
    print(f"✅ Asiento creado: {asiento1.referencia}")
    
    # 10. Crear Certificado de Retención
    print("📋 Creando certificado de retención...")
    certificado = CertificadoRetencion.objects.create(
        tipo='RENTA',
        numero='RET-2024-001',
        fecha=date(2024, 7, 19),
        tercero=dr_carlos,
        base_gravable=Decimal('800000.00'),
        porcentaje_retencion=Decimal('2.50'),
        valor_retenido=Decimal('20000.00'),
        concepto='Retención en la fuente por honorarios médicos',
        creado_por=usuario
    )
    print(f"✅ Certificado creado: {certificado.numero}")
    
    print("\n🎉 ¡Datos de ejemplo creados exitosamente!")
    print("📊 Resumen de datos creados:")
    print(f"   • 1 Empresa")
    print(f"   • {CentroCosto.objects.count()} Centros de Costo")
    print(f"   • 1 Período Contable")
    print(f"   • {CuentaContable.objects.count()} Cuentas Contables")
    print(f"   • {Tercero.objects.count()} Terceros")
    print(f"   • {Diario.objects.count()} Diarios")
    print(f"   • {Impuesto.objects.count()} Impuestos")
    print(f"   • {ComprobanteContable.objects.count()} Comprobantes")
    print(f"   • {AsientoContable.objects.count()} Asientos")
    print(f"   • {LineaAsiento.objects.count()} Líneas de Asiento")
    print(f"   • {CertificadoRetencion.objects.count()} Certificados")
    print("\n🚀 ¡Listo para mostrar a la contadora!")

if __name__ == '__main__':
    crear_datos_ejemplo() 