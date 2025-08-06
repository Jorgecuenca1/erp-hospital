from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ResourceType, ResourceAllocation, StaffSchedule, CapacityPlanning


class ResourceTypeModelTest(TestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Hospital Bed",
            category="room",
            description="Standard hospital bed",
            unit="units",
            is_active=True
        )

    def test_resource_type_creation(self):
        self.assertEqual(self.resource_type.name, "Hospital Bed")
        self.assertEqual(self.resource_type.category, "room")
        self.assertTrue(self.resource_type.is_active)
        self.assertEqual(str(self.resource_type), "Hospital Bed")


class ResourceAllocationModelTest(TestCase):
    def setUp(self):
        self.resource_type = ResourceType.objects.create(
            name="Nurse",
            category="staff",
            unit="hours"
        )
        self.user = User.objects.create_user(
            username="manager",
            password="testpass123"
        )
        self.allocation = ResourceAllocation.objects.create(
            resource_type=self.resource_type,
            department="ICU",
            planned_quantity=40.0,
            allocated_quantity=35.0,
            start_date="2024-01-01",
            end_date="2024-01-31",
            responsible_person=self.user,
            priority="high",
            status="allocated"
        )

    def test_allocation_creation(self):
        self.assertEqual(self.allocation.department, "ICU")
        self.assertEqual(self.allocation.planned_quantity, 40.0)
        self.assertEqual(str(self.allocation), "Nurse - ICU")


class PlanningViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('planning:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Planning") 