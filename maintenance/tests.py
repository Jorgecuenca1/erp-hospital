from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import MedicalEquipment, MaintenanceSchedule, MaintenanceRecord, MaintenanceAlert


class MedicalEquipmentModelTest(TestCase):
    def setUp(self):
        self.equipment = MedicalEquipment.objects.create(
            name="X-Ray Machine",
            equipment_type="Diagnostic",
            model_number="XR-2024",
            serial_number="XR123456",
            manufacturer="Medical Corp",
            purchase_date="2024-01-01",
            location="Radiology Department",
            department="Radiology",
            status="operational"
        )

    def test_equipment_creation(self):
        self.assertEqual(self.equipment.name, "X-Ray Machine")
        self.assertEqual(self.equipment.status, "operational")
        self.assertEqual(str(self.equipment), "X-Ray Machine - XR123456")


class MaintenanceScheduleModelTest(TestCase):
    def setUp(self):
        self.equipment = MedicalEquipment.objects.create(
            name="Test Equipment",
            equipment_type="Medical",
            model_number="TE-001",
            serial_number="TE123",
            manufacturer="Test Corp",
            purchase_date="2024-01-01",
            location="Test Lab",
            department="Testing"
        )
        self.user = User.objects.create_user(
            username="techuser",
            password="testpass123"
        )
        self.schedule = MaintenanceSchedule.objects.create(
            equipment=self.equipment,
            maintenance_type="preventive",
            frequency="monthly",
            next_maintenance="2024-02-01",
            assigned_technician=self.user,
            estimated_duration="02:00:00",
            priority="medium"
        )

    def test_maintenance_schedule_creation(self):
        self.assertEqual(self.schedule.maintenance_type, "preventive")
        self.assertEqual(self.schedule.frequency, "monthly")
        self.assertEqual(str(self.schedule), "Test Equipment - preventive")


class MaintenanceViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('maintenance:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maintenance") 