#!/usr/bin/env python3
"""
Script para crear historias clínicas de prueba
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from admision_recepcion.models import HistoriaClinica, Empresa, Prestador


def crear_historias_clinicas():
    """Crear historias clínicas de prueba con los datos del ejemplo"""
    
    # Obtener empresas y prestadores existentes
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas:
        print("❌ No hay empresas creadas. Ejecute primero crear_datos_admision.py")
        return
    
    if not prestadores:
        print("❌ No hay prestadores creados. Ejecute primero crear_datos_admision.py")
        return
    
    # Usar prestadores existentes o crear algunos básicos
    rosa_pedrozo = prestadores[0] if prestadores else None
    tibisay_ospino = prestadores[1] if len(prestadores) > 1 else prestadores[0] if prestadores else None
    
    if not rosa_pedrozo:
        print("❌ No hay prestadores disponibles")
        return
    
    # Datos de las historias clínicas del ejemplo
    historias_data = [
        {
            'numero_hc': '6934',
            'fecha_creacion': datetime(2025, 8, 8, 9, 47, 48),
            'numero_identificacion': '32.787.620',
            'nombre_paciente': 'MENDEZ SALAS XIOMARA',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_PERIODICO',
            'profesional': rosa_pedrozo,
            'estado': 'ABIERTA'
        },
        {
            'numero_hc': '6933',
            'fecha_creacion': datetime(2025, 8, 8, 9, 20, 15),
            'numero_identificacion': '1.050.396.423',
            'nombre_paciente': 'DIAZ ARIAS NARCISA',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_PERIODICO',
            'profesional': rosa_pedrozo,
            'estado': 'ABIERTA'
        },
        {
            'numero_hc': '6932',
            'fecha_creacion': datetime(2025, 8, 8, 8, 45, 17),
            'numero_identificacion': '1.085.036.335',
            'nombre_paciente': 'RANGEL MARTINEZ DUBERLYS',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6931',
            'fecha_creacion': datetime(2025, 8, 8, 8, 2, 33),
            'numero_identificacion': '85.272.388',
            'nombre_paciente': 'PEINADO PEDROZO JOSE LUIS',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6930',
            'fecha_creacion': datetime(2025, 8, 6, 9, 34, 27),
            'numero_identificacion': '1.003.233.795',
            'nombre_paciente': 'TORRES CASTRO EDWARD ALEJANDRO',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6929',
            'fecha_creacion': datetime(2025, 8, 6, 8, 8, 22),
            'numero_identificacion': '1.085.103.566',
            'nombre_paciente': 'BELEÑO LOPEZ IDERANIS',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6928',
            'fecha_creacion': datetime(2025, 8, 5, 10, 58, 27),
            'numero_identificacion': '22.820.051',
            'nombre_paciente': 'CUETO BELEÑO GLENDA PATRICIA',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_PERIODICO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6927',
            'fecha_creacion': datetime(2025, 8, 5, 10, 44, 46),
            'numero_identificacion': '91.432.949',
            'nombre_paciente': 'MADERA GORDON ALFONSO',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6926',
            'fecha_creacion': datetime(2025, 8, 5, 10, 25, 47),
            'numero_identificacion': '85.273.212',
            'nombre_paciente': 'CANTILLO CARO JUAN CARLOS',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6925',
            'fecha_creacion': datetime(2025, 8, 5, 10, 4, 32),
            'numero_identificacion': '1.129.514.990',
            'nombre_paciente': 'PRADA GIL JOHN EDINSON',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6924',
            'fecha_creacion': datetime(2025, 8, 5, 9, 41, 20),
            'numero_identificacion': '1.007.744.769',
            'nombre_paciente': 'PEREZ VANEGAS ERIKA PATRICIA',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': rosa_pedrozo,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6923',
            'fecha_creacion': datetime(2025, 8, 4, 8, 55, 58),
            'numero_identificacion': '1.002.354.043',
            'nombre_paciente': 'RUBIO COGOLLO JUAN CARLOS',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': tibisay_ospino,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6922',
            'fecha_creacion': datetime(2025, 8, 1, 10, 58, 29),
            'numero_identificacion': '39.019.651',
            'nombre_paciente': 'TAMAYO CASTRO MARTHA VIVIANA',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': tibisay_ospino,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6921',
            'fecha_creacion': datetime(2025, 8, 1, 9, 5, 53),
            'numero_identificacion': '1.085.170.935',
            'nombre_paciente': 'PEDROZO BAENA FERNANDO JOSE',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': tibisay_ospino,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6920',
            'fecha_creacion': datetime(2025, 8, 1, 8, 53, 48),
            'numero_identificacion': '85.442.753',
            'nombre_paciente': 'BANDERA POVEDA ARMANDO',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_INGRESO',
            'profesional': tibisay_ospino,
            'estado': 'CERRADA'
        },
        {
            'numero_hc': '6919',
            'fecha_creacion': datetime(2025, 8, 1, 8, 36, 8),
            'numero_identificacion': '36.577.722',
            'nombre_paciente': 'CANTILLO GONZALEZ NIRLES',
            'tipo_examen': 'EVALUACION_MEDICO_OCUPACIONAL_PERIODICO',
            'profesional': tibisay_ospino,
            'estado': 'CERRADA'
        }
    ]
    
    historias_creadas = 0
    
    for historia_data in historias_data:
        # Verificar si ya existe una historia con ese número
        if not HistoriaClinica.objects.filter(numero_hc=historia_data['numero_hc']).exists():
            
            # Asignar empresa aleatoria
            empresa = random.choice(empresas) if empresas else None
            
            # Calcular fecha de nacimiento aproximada (25-60 años)
            edad_aprox = random.randint(25, 60)
            fecha_nacimiento = date.today() - timedelta(days=edad_aprox * 365)
            
            # Determinar género basado en el nombre
            nombre = historia_data['nombre_paciente']
            if any(name in nombre for name in ['XIOMARA', 'NARCISA', 'GLENDA', 'PATRICIA', 'ERIKA', 'MARTHA']):
                genero = 'F'
            else:
                genero = 'M'
            
            historia = HistoriaClinica.objects.create(
                numero_hc=historia_data['numero_hc'],
                fecha_creacion=timezone.make_aware(historia_data['fecha_creacion']),
                numero_identificacion=historia_data['numero_identificacion'],
                nombre_paciente=historia_data['nombre_paciente'],
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                empresa=empresa,
                tipo_examen=historia_data['tipo_examen'],
                profesional=historia_data['profesional'],
                estado=historia_data['estado'],
                motivo_consulta=f"Evaluación médica ocupacional para {nombre}",
                created_by=admin_user
            )
            
            # Si está cerrada, agregar fecha de cierre
            if historia_data['estado'] == 'CERRADA':
                historia.cerrar_historia(admin_user)
            
            historias_creadas += 1
            print(f"✅ Historia creada: {historia.numero_hc} - {historia.nombre_paciente}")
    
    print(f"\n🎉 Total de historias clínicas creadas: {historias_creadas}")
    
    # Mostrar estadísticas
    total_historias = HistoriaClinica.objects.count()
    abiertas = HistoriaClinica.objects.filter(estado='ABIERTA').count()
    cerradas = HistoriaClinica.objects.filter(estado='CERRADA').count()
    
    print(f"\n📊 Estadísticas de historias clínicas:")
    print(f"   - Total: {total_historias}")
    print(f"   - Abiertas: {abiertas}")
    print(f"   - Cerradas: {cerradas}")
    
    # Estadísticas por profesional
    print(f"\n👩‍⚕️ Por profesional:")
    from django.db.models import Count
    profesionales = HistoriaClinica.objects.values('profesional__nombre').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for prof in profesionales:
        if prof['profesional__nombre']:
            print(f"   - {prof['profesional__nombre']}: {prof['total']} historias")
    
    # Estadísticas por tipo de examen
    print(f"\n🏥 Por tipo de examen:")
    tipos = HistoriaClinica.objects.values('tipo_examen').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for tipo in tipos:
        nombre_tipo = dict(HistoriaClinica.TIPO_EXAMEN_CHOICES).get(tipo['tipo_examen'], tipo['tipo_examen'])
        print(f"   - {nombre_tipo}: {tipo['total']} historias")


if __name__ == '__main__':
    print("🚀 Creando historias clínicas de prueba...")
    crear_historias_clinicas()
    print("\n✅ Proceso completado!")
