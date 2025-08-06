from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from acs_hms_base.models import HMSUser, Patient
import uuid


class WaitingScreen(models.Model):
    """Digital waiting screen configuration"""
    SCREEN_TYPE_CHOICES = [
        ('general', 'General Waiting Area'),
        ('department', 'Department Specific'),
        ('doctor', 'Doctor Specific'),
        ('emergency', 'Emergency'),
    ]
    
    name = models.CharField(max_length=200)
    screen_type = models.CharField(max_length=20, choices=SCREEN_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    
    # Display settings
    display_queue = models.BooleanField(default=True)
    display_announcements = models.BooleanField(default=True)
    display_health_tips = models.BooleanField(default=True)
    display_weather = models.BooleanField(default=False)
    
    # Auto-refresh settings
    refresh_interval = models.IntegerField(default=30, help_text="Refresh interval in seconds")
    
    # Theme settings
    theme_color = models.CharField(max_length=7, default='#007bff')
    logo_file = models.FileField(upload_to='waiting_screens/', null=True, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Waiting Screen'
        verbose_name_plural = 'Waiting Screens'
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class WaitingQueue(models.Model):
    """Patient waiting queue"""
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Queue details
    queue_number = models.CharField(max_length=10)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='waiting_queues')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='waiting_queues', limit_choices_to={'user_type': 'DOCTOR'})
    screen = models.ForeignKey(WaitingScreen, on_delete=models.CASCADE, related_name='queues')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    
    # Timing
    arrival_time = models.DateTimeField(default=timezone.now)
    called_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Estimated wait time
    estimated_wait_minutes = models.IntegerField(default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['arrival_time']
        verbose_name = 'Waiting Queue'
        verbose_name_plural = 'Waiting Queues'
    
    def __str__(self):
        return f"{self.queue_number} - {self.patient.nombre}"
    
    @property
    def wait_time_minutes(self):
        """Calculate current wait time in minutes"""
        if self.status == 'waiting':
            return int((timezone.now() - self.arrival_time).total_seconds() / 60)
        elif self.called_time:
            return int((self.called_time - self.arrival_time).total_seconds() / 60)
        return 0


class ScreenAnnouncement(models.Model):
    """Announcements for waiting screens"""
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('maintenance', 'Maintenance'),
        ('health_tip', 'Health Tip'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPE_CHOICES)
    
    # Display settings
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Priority
    priority = models.IntegerField(default=1, help_text="Higher numbers = higher priority")
    
    # Screens to display on
    screens = models.ManyToManyField(WaitingScreen, related_name='announcements')
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='screen_announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'Screen Announcement'
        verbose_name_plural = 'Screen Announcements'
    
    def __str__(self):
        return self.title


class HealthTip(models.Model):
    """Health tips for waiting screens"""
    CATEGORY_CHOICES = [
        ('general', 'General Health'),
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('mental_health', 'Mental Health'),
        ('preventive', 'Preventive Care'),
        ('seasonal', 'Seasonal Health'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Display settings
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_tips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Health Tip'
        verbose_name_plural = 'Health Tips'
    
    def __str__(self):
        return self.title


class ScreenConfiguration(models.Model):
    """Global configuration for waiting screens"""
    # Default settings
    default_refresh_interval = models.IntegerField(default=30)
    default_theme_color = models.CharField(max_length=7, default='#007bff')
    
    # Display settings
    show_queue_numbers = models.BooleanField(default=True)
    show_wait_times = models.BooleanField(default=True)
    show_doctor_names = models.BooleanField(default=True)
    
    # Audio settings
    enable_audio_announcements = models.BooleanField(default=True)
    audio_language = models.CharField(max_length=10, default='en')
    
    # Health tips settings
    health_tips_interval = models.IntegerField(default=60, help_text="Interval in seconds")
    
    # Metadata
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Screen Configuration'
        verbose_name_plural = 'Screen Configurations'
    
    def __str__(self):
        return f"Screen Configuration - Updated {self.updated_at}"
    
    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and ScreenConfiguration.objects.exists():
            raise ValueError("Only one configuration instance is allowed")
        super().save(*args, **kwargs) 