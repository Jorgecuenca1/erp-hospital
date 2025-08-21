#!/usr/bin/env python
"""
Script de prueba para el módulo de Agenda Electrónica
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from acs_hms_base.models import HMSUser
from acs_hms_online_appointment.models import AgendaElectronicaDisponibilidad, DoctorAvailability
from datetime import date, time, timedelta

def crear_datos_prueba():
    """Crear datos de prueba para el módulo de agenda electrónica"""
    print("🏥 Iniciando creación de datos de prueba para Agenda Electrónica...")
    
    # 1. Crear un usuario y profesional de prueba
    try:
        # Verificar si ya existe el usuario
        user, created = User.objects.get_or_create(
            username='dr_prueba',
            defaults={
                'first_name': 'Doctor',
                'last_name': 'de Prueba',
                'email': 'doctor.prueba@hospital.com',
                'is_active': True
            }
        )
        
        if created:
            user.set_password('123456')
            user.save()
            print(f"✅ Usuario creado: {user.get_full_name()}")
        else:
            print(f"ℹ️ Usuario ya existe: {user.get_full_name()}")
        
        # Verificar/crear hospital y departamento requeridos
        from acs_hms_base.models import Hospital, Department
        
        hospital, _ = Hospital.objects.get_or_create(
            name='Hospital de Prueba',
            defaults={
                'code': 'HP001',
                'address': 'Calle Principal 123',
                'city': 'Ciudad Prueba',
                'state': 'Estado Prueba',
                'country': 'Colombia',
                'zip_code': '110111',
                'phone': '+57123456789',
                'email': 'contacto@hospitalprueba.com',
                'license_number': 'LIC123456',
                'established_date': date(2020, 1, 1),
                'registration_number': 'REG789012',
                'active': True
            }
        )
        
        department, _ = Department.objects.get_or_create(
            name='Medicina General',
            hospital=hospital,
            defaults={
                'code': 'MG001',
                'description': 'Departamento de Medicina General',
                'location': 'Piso 1',
                'active': True
            }
        )
        
        # Crear HMS User (Doctor)
        hms_user, created = HMSUser.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': f'DOC{user.id:04d}',
                'user_type': 'DOCTOR',
                'hospital': hospital,
                'department': department,
                'active': True
            }
        )
        
        if created:
            print(f"✅ HMSUser (Doctor) creado: {hms_user}")
        else:
            print(f"ℹ️ HMSUser ya existe: {hms_user}")
            
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False
    
    # 2. Crear disponibilidad en agenda electrónica
    try:
        fecha_desde = date.today()
        fecha_hasta = fecha_desde + timedelta(days=30)
        
        agenda, created = AgendaElectronicaDisponibilidad.objects.get_or_create(
            profesional=hms_user,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            defaults={
                'hora_inicio_am': time(8, 0),
                'hora_fin_am': time(12, 0),
                'hora_inicio_pm': time(14, 0),
                'hora_fin_pm': time(18, 0),
                'dividir_en': 30,
                'sede': 'PRINCIPAL',
                'lunes': True,
                'martes': True,
                'miercoles': True,
                'jueves': True,
                'viernes': True,
                'sabado': False,
                'domingo': False,
                'habilitar_agenda_tus_citas': True,
                'habilitar_doctoralia': True,
                'status': 'active',
                'created_by': user
            }
        )
        
        if created:
            print(f"✅ Agenda electrónica creada: {agenda}")
            
            # Generar slots de disponibilidad
            slots_creados = agenda.generar_slots_disponibilidad()
            print(f"✅ {slots_creados} slots de disponibilidad generados")
            
        else:
            print(f"ℹ️ Agenda electrónica ya existe: {agenda}")
            
    except Exception as e:
        print(f"❌ Error creando agenda electrónica: {e}")
        return False
    
    # 3. Verificar disponibilidades creadas
    try:
        availabilities = DoctorAvailability.objects.filter(doctor=hms_user)
        print(f"📊 Total disponibilidades creadas: {availabilities.count()}")
        
        for avail in availabilities:
            print(f"   - {avail.get_day_of_week_display()}: {avail.start_time} - {avail.end_time} ({avail.sede})")
            
    except Exception as e:
        print(f"❌ Error verificando disponibilidades: {e}")
        return False
    
    print("\n🎉 ¡Datos de prueba creados exitosamente!")
    print("\n📋 Resumen:")
    print(f"   • Usuario: {user.get_full_name()} ({user.username})")
    print(f"   • Profesional: {hms_user}")
    print(f"   • Agenda: {agenda}")
    print(f"   • Período: {agenda.fecha_desde} - {agenda.fecha_hasta}")
    print(f"   • Horarios: AM {agenda.hora_inicio_am}-{agenda.hora_fin_am}, PM {agenda.hora_inicio_pm}-{agenda.hora_fin_pm}")
    print(f"   • Días: {', '.join(agenda.get_dias_seleccionados())}")
    print(f"   • Sede: {agenda.get_sede_display()}")
    print(f"   • Integraciones: {'Agenda tus citas' if agenda.habilitar_agenda_tus_citas else ''} {'Doctoralia' if agenda.habilitar_doctoralia else ''}")
    print(f"   • Slots generados: {agenda.slots_generados}")
    
    return True

def verificar_sistema():
    """Verificar que el sistema está funcionando correctamente"""
    print("\n🔍 Verificando el sistema...")
    
    try:
        # Verificar modelos
        total_agendas = AgendaElectronicaDisponibilidad.objects.count()
        total_availabilities = DoctorAvailability.objects.count()
        total_doctors = HMSUser.objects.filter(user_type='DOCTOR').count()
        
        print(f"📊 Estadísticas del sistema:")
        print(f"   • Total agendas electrónicas: {total_agendas}")
        print(f"   • Total disponibilidades: {total_availabilities}")
        print(f"   • Total doctores: {total_doctors}")
        
        # Verificar integraciones
        agendas_con_agenda_tus_citas = AgendaElectronicaDisponibilidad.objects.filter(habilitar_agenda_tus_citas=True).count()
        agendas_con_doctoralia = AgendaElectronicaDisponibilidad.objects.filter(habilitar_doctoralia=True).count()
        
        print(f"   • Agendas con 'Agenda tus citas': {agendas_con_agenda_tus_citas}")
        print(f"   • Agendas con 'Doctoralia': {agendas_con_doctoralia}")
        
        print("✅ Sistema verificado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando sistema: {e}")
        return False

def mostrar_urls():
    """Mostrar las URLs disponibles para probar"""
    print("\n🌐 URLs disponibles para probar:")
    print("   📱 Dashboard: http://localhost:8000/hms/online-appointment/")
    print("   📅 Agenda Electrónica (Lista): http://localhost:8000/hms/online-appointment/agenda/")
    print("   ➕ Crear Disponibilidad: http://localhost:8000/hms/online-appointment/agenda/crear/")
    print("   🔧 Gestión de Horarios: http://localhost:8000/hms/online-appointment/availability/")
    print("   👤 Admin Django: http://localhost:8000/admin/")
    print("\n📝 Para acceder al admin, use:")
    print("   Usuario: admin")
    print("   Contraseña: (crear superusuario con 'python manage.py createsuperuser')")

if __name__ == "__main__":
    print("🏥 HMetaHIS - Test de Agenda Electrónica")
    print("=" * 50)
    
    # Crear datos de prueba
    if crear_datos_prueba():
        # Verificar sistema
        verificar_sistema()
        
        # Mostrar URLs
        mostrar_urls()
        
        print("\n🚀 ¡Sistema listo para usar!")
        print("\nPara iniciar el servidor de desarrollo:")
        print("   python manage.py runserver")
        
    else:
        print("\n❌ Error en la creación de datos de prueba")
        sys.exit(1)
