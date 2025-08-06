from django.apps import AppConfig


class EsgReportingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esg_reporting'
    verbose_name = 'ESG Reporting'
    
    def ready(self):
        """Initialize ESG reporting system"""
        pass 