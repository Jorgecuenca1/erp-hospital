from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ExpenseCategory, ExpenseReport, ExpenseItem, ExpensePolicy, ExpenseApproval


class ExpenseCategoryModelTest(TestCase):
    def setUp(self):
        self.category = ExpenseCategory.objects.create(
            name="Travel Expenses",
            code="TRAVEL",
            description="Business travel related expenses",
            is_active=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Travel Expenses")
        self.assertEqual(self.category.code, "TRAVEL")
        self.assertTrue(self.category.is_active)
        self.assertEqual(str(self.category), "Travel Expenses")


class ExpenseReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="employee",
            password="testpass123"
        )
        self.report = ExpenseReport.objects.create(
            employee=self.user,
            report_number="EXP-001",
            title="Business Trip Expenses",
            description="Expenses for medical conference",
            submit_date="2024-01-15",
            total_amount=500.00,
            currency="USD",
            status="submitted"
        )

    def test_report_creation(self):
        self.assertEqual(self.report.report_number, "EXP-001")
        self.assertEqual(self.report.total_amount, 500.00)
        self.assertEqual(self.report.status, "submitted")
        self.assertEqual(str(self.report), "EXP-001 - employee")


class ExpenseManagementViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('expense_management:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Expense") 