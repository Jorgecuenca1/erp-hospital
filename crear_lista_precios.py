#!/usr/bin/env python3
"""
Script para crear la lista de precios con datos del ejemplo mostrado
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from admision_recepcion.models import ListaPrecios, Convenio


def crear_lista_precios():
    """Crear lista de precios con datos del ejemplo"""
    
    # Datos exactos del ejemplo mostrado
    productos_data = [
        {
            'nombre': 'ACTIVIDADES DE PROMOCION Y PREVENSION DE SEGURIDAD Y SALUD EN EL TRABAJO',
            'precio': 0,
            'cups': '',
            'rips': 'OTROS_SERVICIOS',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'Ajuste Por Nota Crédito Sin Referencia a Factura',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'ADMINISTRATIVOS'
        },
        {
            'nombre': 'Ajuste Por Nota Débito',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'ADMINISTRATIVOS'
        },
        {
            'nombre': 'ALCOHOLEMIA',
            'precio': 165000,
            'cups': '',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'Anticipo',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'ADMINISTRATIVOS'
        },
        {
            'nombre': 'ANTIGENO SUPERFICIE HEPATITIS B',
            'precio': 70000,
            'cups': '906221',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'AUDIOMETRIA',
            'precio': 30000,
            'cups': '954102',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'BK BACILOS COPIA',
            'precio': 25000,
            'cups': '901101',
            'rips': '',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'BUN',
            'precio': 20000,
            'cups': '',
            'rips': 'OTROS_SERVICIOS',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'BUN CREATININA',
            'precio': 30000,
            'cups': '',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'COCAÍNA + MARIHUANA',
            'precio': 100000,
            'cups': '905727',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'COLESTEROL HDL',
            'precio': 5000,
            'cups': '903815',
            'rips': 'OTROS_SERVICIOS',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'COLESTEROL TOTAL',
            'precio': 25000,
            'cups': '903818',
            'rips': '',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'COLINESTERASA ERITROCITARIA',
            'precio': 105000,
            'cups': '903419',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'Copago',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'ADMINISTRATIVOS'
        },
        {
            'nombre': 'COPROLOGICO',
            'precio': 20000,
            'cups': '907002',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'CREATININA',
            'precio': 18000,
            'cups': '903825',
            'rips': 'OTROS_SERVICIOS',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'Cuestionario Covid - 19',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'OTROS'
        },
        {
            'nombre': 'Cuota Moderadora',
            'precio': 1,
            'cups': '',
            'rips': '',
            'iva': 0.00,
            'categoria': 'ADMINISTRATIVOS'
        },
        {
            'nombre': 'DROGAS',
            'precio': 0,
            'cups': '',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        # Agregamos más servicios comunes
        {
            'nombre': 'EXAMEN MÉDICO OCUPACIONAL INGRESO',
            'precio': 85000,
            'cups': '890201',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'EXAMEN MÉDICO OCUPACIONAL PERIÓDICO',
            'precio': 75000,
            'cups': '890202',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'EXAMEN MÉDICO OCUPACIONAL RETIRO',
            'precio': 80000,
            'cups': '890203',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'VISIOMETRÍA',
            'precio': 25000,
            'cups': '954201',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'ESPIROMETRÍA',
            'precio': 45000,
            'cups': '954301',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'ELECTROCARDIOGRAMA',
            'precio': 35000,
            'cups': '948101',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'IMAGENES'
        },
        {
            'nome': 'RADIOGRAFÍA DE TÓRAX PA',
            'precio': 55000,
            'cups': '942101',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'IMAGENES'
        },
        {
            'nombre': 'EXAMEN TRABAJO EN ALTURAS',
            'precio': 120000,
            'cups': '890250',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'EXAMEN ESPACIOS CONFINADOS',
            'precio': 110000,
            'cups': '890251',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'EXAMENES_OCUPACIONALES'
        },
        {
            'nombre': 'HEMOGRAMA COMPLETO',
            'precio': 22000,
            'cups': '901212',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'GLICEMIA EN AYUNAS',
            'precio': 12000,
            'cups': '903841',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'ÁCIDO ÚRICO',
            'precio': 15000,
            'cups': '903824',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'TRIGLICÉRIDOS',
            'precio': 18000,
            'cups': '903819',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'PARCIAL DE ORINA',
            'precio': 15000,
            'cups': '904101',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'CONSULTA MEDICINA GENERAL',
            'precio': 65000,
            'cups': '890301',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'CONSULTAS'
        },
        {
            'nombre': 'CONSULTA MEDICINA ESPECIALIZADA',
            'precio': 95000,
            'cups': '890302',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'CONSULTAS'
        },
        {
            'nombre': 'OPTOMETRÍA',
            'precio': 40000,
            'cups': '954401',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'CONSULTAS'
        },
        {
            'nombre': 'PSICOLOGÍA OCUPACIONAL',
            'precio': 55000,
            'cups': '890801',
            'rips': 'CONSULTA',
            'iva': 0.00,
            'categoria': 'CONSULTAS'
        },
        {
            'nombre': 'FOSFATASA ALCALINA',
            'precio': 16000,
            'cups': '903827',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'BILIRRUBINAS TOTAL Y DIRECTA',
            'precio': 20000,
            'cups': '903828',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        },
        {
            'nombre': 'TRANSAMINASAS (TGO - TGP)',
            'precio': 28000,
            'cups': '903829',
            'rips': 'PROCEDIMIENTO',
            'iva': 0.00,
            'categoria': 'LABORATORIO'
        }
    ]
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    
    productos_creados = 0
    
    for producto_data in productos_data:
        # Corregir typo en el nombre
        if 'nome' in producto_data:
            producto_data['nombre'] = producto_data.pop('nome')
        
        # Verificar si ya existe
        if not ListaPrecios.objects.filter(nombre_producto_servicio=producto_data['nombre']).exists():
            
            producto = ListaPrecios.objects.create(
                nombre_producto_servicio=producto_data['nombre'],
                precio=producto_data['precio'],
                codigo_cups=producto_data['cups'],
                tipo_rips=producto_data['rips'],
                porcentaje_iva=producto_data['iva'],
                gravado_iva=producto_data['iva'] > 0,
                categoria=producto_data['categoria'],
                activo=True,
                generar_rips=bool(producto_data['rips']),
                created_by=admin_user
            )
            
            productos_creados += 1
            print(f"✅ Producto creado: {producto.codigo_interno} - {producto.nombre_producto_servicio[:50]}...")
    
    print(f"\n🎉 Total de productos creados: {productos_creados}")
    
    # Mostrar resumen por categorías
    print("\n📊 Resumen por categorías:")
    from django.db.models import Count
    categorias = ListaPrecios.objects.values('categoria').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for categoria in categorias:
        print(f"   - {categoria['categoria']}: {categoria['total']} productos")
    
    # Mostrar estadísticas
    total_productos = ListaPrecios.objects.count()
    con_cups = ListaPrecios.objects.exclude(codigo_cups='').count()
    con_rips = ListaPrecios.objects.exclude(tipo_rips='').count()
    valor_total = sum(p.precio for p in ListaPrecios.objects.all())
    
    print(f"\n📈 Estadísticas generales:")
    print(f"   - Total productos: {total_productos}")
    print(f"   - Con código CUPS: {con_cups}")
    print(f"   - Con tipo RIPS: {con_rips}")
    print(f"   - Valor total lista: ${valor_total:,.0f}")
    
    print("\n📋 Lista de precios creada exitosamente!")
    print("   - Los productos están listos para ser utilizados")
    print("   - Los códigos CUPS están configurados para RIPS")
    print("   - Puede asociar convenios desde el panel de administración")


if __name__ == '__main__':
    print("🚀 Creando lista de precios...")
    crear_lista_precios()
    print("\n✅ Proceso completado!")
