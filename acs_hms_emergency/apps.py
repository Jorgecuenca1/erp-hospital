from django.apps import AppConfig


class AcsHmsEmergencyConfig(AppConfig):
    name = 'acs_hms_emergency'
    verbose_name = 'HMS Emergency & Ambulance Services'
    
    def ready(self):
        import acs_hms_emergency.signals 