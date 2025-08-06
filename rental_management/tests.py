from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import RentalEquipment, RentalAgreement, RentalPayment, RentalInspection


class RentalEquipmentModelTest(TestCase):
    def setUp(self):
        self.equipment = RentalEquipment.objects.create(
            name="Portable Ultrasound",
            category="diagnostic",
            model="US-2024",
            manufacturer="Medical Devices Inc",
            serial_number="US123456",
            description="Portable ultrasound machine",
            daily_rate=150.00,
            weekly_rate=900.00,
            monthly_rate=3000.00,
            security_deposit=500.00,
            availability_status="available",
            location="Equipment Storage"
        )

    def test_equipment_creation(self):
        self.assertEqual(self.equipment.name, "Portable Ultrasound")
        self.assertEqual(self.equipment.daily_rate, 150.00)
        self.assertEqual(self.equipment.availability_status, "available")
        self.assertEqual(str(self.equipment), "Portable Ultrasound - US123456")


class RentalAgreementModelTest(TestCase):
    def setUp(self):
        self.equipment = RentalEquipment.objects.create(
            name="Test Equipment",
            category="diagnostic",
            model="TE-001",
            manufacturer="Test Corp",
            serial_number="TE123",
            daily_rate=100.00,
            weekly_rate=600.00,
            monthly_rate=2000.00,
            security_deposit=300.00
        )
        self.user = User.objects.create_user(
            username="staff",
            password="testpass123"
        )
        self.agreement = RentalAgreement.objects.create(
            agreement_number="RA-001",
            equipment=self.equipment,
            renter_name="Test Hospital",
            renter_contact="555-1234",
            renter_address="123 Medical St",
            start_date="2024-01-01",
            end_date="2024-01-31",
            rental_period="monthly",
            rental_rate=2000.00,
            total_amount=2300.00,
            security_deposit=300.00,
            status="active",
            created_by=self.user
        )

    def test_agreement_creation(self):
        self.assertEqual(self.agreement.agreement_number, "RA-001")
        self.assertEqual(self.agreement.total_amount, 2300.00)
        self.assertEqual(self.agreement.status, "active")
        self.assertEqual(str(self.agreement), "RA-001 - Test Equipment")


class RentalManagementViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('rental_management:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rental") 