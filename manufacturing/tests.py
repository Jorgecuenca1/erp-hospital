from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import MedicalDevice, ProductionOrder, QualityCheck, BillOfMaterials


class MedicalDeviceModelTest(TestCase):
    def setUp(self):
        self.device = MedicalDevice.objects.create(
            name="Test MRI Machine",
            device_type="Diagnostic",
            model_number="MRI-2024",
            manufacturer="Medical Corp",
            serial_number="MRI123456",
            manufacturing_date="2024-01-01",
            status="active"
        )

    def test_device_creation(self):
        self.assertEqual(self.device.name, "Test MRI Machine")
        self.assertEqual(self.device.status, "active")
        self.assertEqual(str(self.device), "Test MRI Machine - MRI123456")


class ProductionOrderModelTest(TestCase):
    def setUp(self):
        self.device = MedicalDevice.objects.create(
            name="Test Device",
            device_type="Medical",
            model_number="TD-001",
            manufacturer="Test Corp",
            serial_number="TD123",
            manufacturing_date="2024-01-01"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.order = ProductionOrder.objects.create(
            order_number="PO-001",
            device=self.device,
            quantity=10,
            priority="medium",
            status="draft",
            assigned_to=self.user,
            start_date="2024-01-01T10:00:00Z"
        )

    def test_production_order_creation(self):
        self.assertEqual(self.order.order_number, "PO-001")
        self.assertEqual(self.order.quantity, 10)
        self.assertEqual(str(self.order), "Order PO-001 - Test Device")


class ManufacturingViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('manufacturing:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manufacturing")

    def test_device_list_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('manufacturing:device_list'))
        self.assertEqual(response.status_code, 200) 