#!/usr/bin/env python3
"""
Script para crear audiometrías de prueba
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from admision_recepcion.models import (
    FichaClinica, Audiometria, Empresa, Prestador, Municipio,
    AntecedenteAuditivo, AntecedenteAuditivoLaboral, DiagnosticoAuditivo, RecomendacionAuditiva
)


def crear_audiometrias():
    """Crear audiometrías de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de trabajadores para audiometría
    trabajadores_data = [
        {
            'numero_identificacion': '30.123.456.789',
            'nombre_trabajador': 'JUAN CARLOS MARTINEZ LOPEZ',
            'genero': 'M',
            'edad': 28,
            'cargo': 'Operario de Máquinas',
            'funciones_cargo': 'Operación de maquinaria industrial con exposición a ruido',
            'exposicion_anos': 5,
            'exposicion_meses': 3
        },
        {
            'numero_identificacion': '25.234.567.890',
            'nombre_trabajador': 'MARIA FERNANDA GUTIERREZ ROJAS',
            'genero': 'F',
            'edad': 35,
            'cargo': 'Supervisora de Producción',
            'funciones_cargo': 'Supervisión de área de producción con ruido moderado',
            'exposicion_anos': 8,
            'exposicion_meses': 6
        },
        {
            'numero_identificacion': '18.345.678.901',
            'nombre_trabajador': 'PEDRO ANTONIO SILVA MENDOZA',
            'genero': 'M',
            'edad': 42,
            'cargo': 'Soldador',
            'funciones_cargo': 'Soldadura y corte con equipos de alta potencia',
            'exposicion_anos': 15,
            'exposicion_meses': 2
        },
        {
            'numero_identificacion': '42.456.789.012',
            'nombre_trabajador': 'CAROLINA ISABEL HERRERA CASTRO',
            'genero': 'F',
            'edad': 31,
            'cargo': 'Técnica de Laboratorio',
            'funciones_cargo': 'Manejo de equipos de laboratorio con emisión sonora mínima',
            'exposicion_anos': 3,
            'exposicion_meses': 8
        },
        {
            'numero_identificacion': '15.567.890.123',
            'nombre_trabajador': 'RICARDO JOSE PEÑA VALDERRAMA',
            'genero': 'M',
            'edad': 39,
            'cargo': 'Mecánico Industrial',
            'funciones_cargo': 'Mantenimiento de maquinaria pesada con herramientas neumáticas',
            'exposicion_anos': 12,
            'exposicion_meses': 4
        }
    ]
    
    audiometrias_creadas = 0
    
    for trabajador_data in trabajadores_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=trabajador_data['numero_identificacion'],
            tipo_ficha='AUDIOMETRIA'
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='AUDIOMETRIA',
                fecha_evaluacion=date.today(),
                numero_identificacion=trabajador_data['numero_identificacion'],
                nombre_trabajador=trabajador_data['nombre_trabajador'],
                genero=trabajador_data['genero'],
                edad=trabajador_data['edad'],
                fecha_nacimiento=date.today() - timedelta(days=trabajador_data['edad'] * 365),
                empresa=random.choice(empresas),
                cargo=trabajador_data['cargo'],
                profesional_evaluador=random.choice(prestadores),
                municipio=municipios[0] if municipios else None,
                estado='PENDIENTE',
                created_by=admin_user
            )
            
            # Generar datos audiométricos realistas
            # Simulamos diferentes tipos de pérdida auditiva
            edad = trabajador_data['edad']
            exposicion_total = trabajador_data['exposicion_anos']
            
            # Función para simular umbrales auditivos
            def generar_umbrales(base_threshold=5, noise_damage=0, age_factor=0):
                """Generar umbrales audiométricos realistas"""
                # Frecuencias estándar
                frecuencias = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
                umbrales = {}
                
                for freq in frecuencias:
                    # Umbral base
                    umbral = base_threshold
                    
                    # Daño por ruido (más pronunciado en 4000-6000 Hz)
                    if freq in [4000, 6000]:
                        umbral += noise_damage * 1.5
                    elif freq in [3000, 8000]:
                        umbral += noise_damage * 1.2
                    else:
                        umbral += noise_damage * 0.8
                    
                    # Factor de edad (presbiacusia)
                    if freq >= 4000:
                        umbral += age_factor * (freq / 1000)
                    
                    # Agregar variabilidad natural
                    umbral += random.randint(-5, 10)
                    
                    # Mantener en rango realista
                    umbral = max(0, min(120, umbral))
                    umbrales[freq] = int(umbral)
                
                return umbrales
            
            # Calcular factores de daño
            noise_damage = exposicion_total * 2  # Factor de exposición
            age_factor = max(0, (edad - 25) * 0.5)  # Factor de edad
            
            # Generar umbrales para oído derecho
            umbrales_od = generar_umbrales(
                base_threshold=random.randint(0, 10),
                noise_damage=noise_damage,
                age_factor=age_factor
            )
            
            # Generar umbrales para oído izquierdo (ligeramente diferentes)
            umbrales_oi = generar_umbrales(
                base_threshold=random.randint(0, 10),
                noise_damage=noise_damage * random.uniform(0.8, 1.2),
                age_factor=age_factor
            )
            
            # Crear audiometría
            audiometria = Audiometria.objects.create(
                ficha_clinica=ficha,
                producto='Audiometría Ocupacional',
                funciones_cargo=trabajador_data['funciones_cargo'],
                eps=random.choice(['EPS Sura', 'Salud Total', 'Nueva EPS', 'Compensar']),
                descanso_auditivo_horas=random.choice([12, 14, 16, 24]),
                realizo_retest=random.choice([True, False]),
                uso_cabina_sonoamortiguada=True,
                marca_audiometro=random.choice([
                    'Interacoustics AD629', 'Madsen Astera²', 'GSI AudioStar Pro',
                    'Amplivox 270', 'Maico MA 25'
                ]),
                fecha_ultima_calibracion=date.today() - timedelta(days=random.randint(30, 365)),
                
                # Otoscopia
                otoscopia_oido_derecho='Conducto auditivo externo permeable, sin cerumen impactado. Membrana timpánica íntegra.',
                otoscopia_oido_izquierdo='Conducto auditivo externo permeable, sin cerumen impactado. Membrana timpánica íntegra.',
                
                # Vía Aérea - Oído Derecho
                va_od_250=umbrales_od[250],
                va_od_500=umbrales_od[500],
                va_od_1000=umbrales_od[1000],
                va_od_2000=umbrales_od[2000],
                va_od_3000=umbrales_od[3000],
                va_od_4000=umbrales_od[4000],
                va_od_6000=umbrales_od[6000],
                va_od_8000=umbrales_od[8000],
                
                # Vía Aérea - Oído Izquierdo
                va_oi_250=umbrales_oi[250],
                va_oi_500=umbrales_oi[500],
                va_oi_1000=umbrales_oi[1000],
                va_oi_2000=umbrales_oi[2000],
                va_oi_3000=umbrales_oi[3000],
                va_oi_4000=umbrales_oi[4000],
                va_oi_6000=umbrales_oi[6000],
                va_oi_8000=umbrales_oi[8000],
                
                # Vía Ósea (generalmente 10-15 dB mejor que vía aérea)
                vo_od_250=max(0, umbrales_od[250] - random.randint(10, 15)),
                vo_od_500=max(0, umbrales_od[500] - random.randint(10, 15)),
                vo_od_1000=max(0, umbrales_od[1000] - random.randint(10, 15)),
                vo_od_2000=max(0, umbrales_od[2000] - random.randint(10, 15)),
                vo_od_3000=max(0, umbrales_od[3000] - random.randint(10, 15)),
                vo_od_4000=max(0, umbrales_od[4000] - random.randint(10, 15)),
                
                vo_oi_250=max(0, umbrales_oi[250] - random.randint(10, 15)),
                vo_oi_500=max(0, umbrales_oi[500] - random.randint(10, 15)),
                vo_oi_1000=max(0, umbrales_oi[1000] - random.randint(10, 15)),
                vo_oi_2000=max(0, umbrales_oi[2000] - random.randint(10, 15)),
                vo_oi_3000=max(0, umbrales_oi[3000] - random.randint(10, 15)),
                vo_oi_4000=max(0, umbrales_oi[4000] - random.randint(10, 15)),
                
                observaciones='Audiometría realizada en condiciones adecuadas de calibración y ambiente.'
            )
            
            # La severidad se calcula automáticamente en el método save()
            
            # Crear antecedentes auditivos por defecto
            antecedentes_types = [
                'OTITIS', 'TRAUMA', 'CIRUGIA', 'INGESTA_OTOTOXICOS',
                'HIPOACUSIA_SUBJETIVA', 'ACUFENOS', 'TEJO', 'MOTO',
                'DISCOTECA', 'SERVICIO_MILITAR', 'POLIGONO', 'AUDIFONOS'
            ]
            
            for antecedente_type in antecedentes_types:
                observacion = 'NO REFIERE'
                # Algunos antecedentes positivos ocasionales
                if antecedente_type in ['AUDIFONOS', 'MOTO'] and random.random() < 0.3:
                    observacion = 'Uso ocasional'
                elif antecedente_type == 'DISCOTECA' and random.random() < 0.4:
                    observacion = 'Exposición esporádica'
                
                AntecedenteAuditivo.objects.create(
                    audiometria=audiometria,
                    tipo_antecedente=antecedente_type,
                    observacion=observacion
                )
            
            # Crear antecedente auditivo laboral
            AntecedenteAuditivoLaboral.objects.create(
                audiometria=audiometria,
                empresa=ficha.empresa.razon_social,
                cargo=trabajador_data['cargo'],
                tipo_proteccion=random.choice(['TAPONES_ESPUMA', 'PROTECTORES_COPA', 'TAPONES_SILICONA']),
                tolerancia_proteccion=random.choice(['BUENA', 'REGULAR', 'BUENA', 'BUENA']),  # Más probabilidad de buena
                tiempo_exposicion_anos=trabajador_data['exposicion_anos'],
                tiempo_exposicion_meses=trabajador_data['exposicion_meses']
            )
            
            # Crear recomendaciones por defecto
            recomendaciones_default = [
                ('CONTROL_AUDITIVO_1_ANO', True),
                ('USE_PROTECCION_AUDITIVA', True),
                ('CONTROL_AUDITIVO_6_MESES', False),
                ('CONTROL_OTORRINO', False),
                ('AUDIOMETRIA_CONFIRMATORIA', False),
            ]
            
            # Modificar recomendaciones según severidad
            severidad_od = audiometria.calcular_severidad_od()
            severidad_oi = audiometria.calcular_severidad_oi()
            
            if severidad_od in ['MODERADA', 'SEVERA'] or severidad_oi in ['MODERADA', 'SEVERA']:
                recomendaciones_default[2] = ('CONTROL_AUDITIVO_6_MESES', True)  # Control en 6 meses
                recomendaciones_default[3] = ('CONTROL_OTORRINO', True)  # Control por otorrino
            
            for codigo, seleccionado in recomendaciones_default:
                RecomendacionAuditiva.objects.create(
                    audiometria=audiometria,
                    codigo=codigo,
                    seleccionado=seleccionado
                )
            
            audiometrias_creadas += 1
            print(f"✅ Audiometría creada: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
            print(f"   📊 Severidad OD: {audiometria.severidad_od}, OI: {audiometria.severidad_oi}")
    
    print(f"\n🎉 Total de audiometrías creadas: {audiometrias_creadas}")
    
    # Mostrar estadísticas
    total_audiometrias = Audiometria.objects.count()
    
    print(f"\n📊 Estadísticas de audiometrías:")
    print(f"   - Total audiometrías: {total_audiometrias}")
    
    # Estadísticas por severidad
    from django.db.models import Count
    severidad_stats = Audiometria.objects.values('severidad_od').annotate(
        total=Count('id')
    ).order_by('severidad_od')
    
    print(f"\n🔊 Severidad OD:")
    for stat in severidad_stats:
        severidad_display = dict(Audiometria.SEVERIDAD_CAOHC_CHOICES).get(stat['severidad_od'], stat['severidad_od'])
        print(f"   - {severidad_display}: {stat['total']} casos")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    empresas_stats = FichaClinica.objects.filter(
        tipo_ficha='AUDIOMETRIA',
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} audiometrías")
    
    # Estadísticas por profesional
    print(f"\n👨‍⚕️ Por profesional:")
    profesionales_stats = FichaClinica.objects.filter(
        tipo_ficha='AUDIOMETRIA',
        profesional_evaluador__isnull=False
    ).values('profesional_evaluador__nombre').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for profesional in profesionales_stats:
        print(f"   - {profesional['profesional_evaluador__nombre']}: {profesional['total']} audiometrías")


if __name__ == '__main__':
    print("🔊 Creando audiometrías de prueba...")
    crear_audiometrias()
    print("\n✅ Proceso completado!")
