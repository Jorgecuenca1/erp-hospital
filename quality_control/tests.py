from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import QualityStandard, QualityAudit, QualityMetric, IncidentReport, QualityImprovement


class QualityStandardModelTest(TestCase):
    def setUp(self):
        self.standard = QualityStandard.objects.create(
            name="Patient Safety Standard",
            category="patient_safety",
            description="Standard for patient safety measures",
            target_value=95.0,
            unit="percentage",
            frequency="monthly",
            is_active=True
        )

    def test_standard_creation(self):
        self.assertEqual(self.standard.name, "Patient Safety Standard")
        self.assertEqual(self.standard.target_value, 95.0)
        self.assertTrue(self.standard.is_active)
        self.assertEqual(str(self.standard), "Patient Safety Standard")


class IncidentReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reporter",
            password="testpass123"
        )
        self.incident = IncidentReport.objects.create(
            incident_type="patient_safety",
            severity="medium",
            department="Emergency",
            reporter=self.user,
            incident_date="2024-01-01T10:00:00Z",
            description="Test incident description",
            immediate_action="Immediate action taken",
            status="reported"
        )

    def test_incident_creation(self):
        self.assertEqual(self.incident.incident_type, "patient_safety")
        self.assertEqual(self.incident.severity, "medium")
        self.assertEqual(self.incident.department, "Emergency")
        self.assertEqual(str(self.incident), "patient_safety - 2024-01-01 10:00:00+00:00")


class QualityControlViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('quality_control:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quality Control") 