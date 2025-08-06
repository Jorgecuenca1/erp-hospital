from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class WebcamDevice(models.Model):
    """Webcam devices registered in the system"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('offline', 'Offline'),
        ('error', 'Error'),
    ]
    
    DEVICE_TYPE_CHOICES = [
        ('consultation', 'Consultation Camera'),
        ('security', 'Security Camera'),
        ('monitoring', 'Patient Monitoring'),
        ('surgical', 'Surgical Camera'),
        ('mobile', 'Mobile Camera'),
        ('desktop', 'Desktop Camera'),
    ]
    
    device_id = models.CharField(max_length=20, unique=True, blank=True)
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES, default='consultation')
    
    # Technical specifications
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Camera specifications
    resolution = models.CharField(max_length=50, default='1920x1080')
    fps = models.IntegerField(default=30, validators=[MinValueValidator(1), MaxValueValidator(60)])
    has_audio = models.BooleanField(default=True)
    has_zoom = models.BooleanField(default=False)
    zoom_capability = models.CharField(max_length=50, blank=True)
    
    # Network information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=17, blank=True)
    port = models.IntegerField(default=80)
    
    # Authentication
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    
    # Status and monitoring
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_ping = models.DateTimeField(null=True, blank=True)
    uptime_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Assigned personnel
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_webcams')
    
    # Maintenance
    last_maintenance = models.DateTimeField(null=True, blank=True)
    next_maintenance = models.DateTimeField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    
    # Settings
    is_recording_enabled = models.BooleanField(default=False)
    is_streaming_enabled = models.BooleanField(default=True)
    is_motion_detection_enabled = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['device_name']
        verbose_name = 'Webcam Device'
        verbose_name_plural = 'Webcam Devices'
    
    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = f"WC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.device_name} ({self.device_id})"
    
    @property
    def is_online(self):
        if self.last_ping:
            return (timezone.now() - self.last_ping).total_seconds() < 300  # 5 minutes
        return False


class WebcamSession(models.Model):
    """Webcam streaming/recording sessions"""
    SESSION_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('telemedicine', 'Telemedicine'),
        ('monitoring', 'Patient Monitoring'),
        ('recording', 'Recording'),
        ('security', 'Security'),
        ('surgery', 'Surgery'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    session_id = models.CharField(max_length=20, unique=True, blank=True)
    webcam_device = models.ForeignKey(WebcamDevice, on_delete=models.CASCADE, related_name='sessions')
    
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Session participants
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    
    # Session details
    session_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Timing
    scheduled_start = models.DateTimeField(null=True, blank=True)
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Recording settings
    is_recording = models.BooleanField(default=False)
    record_video = models.BooleanField(default=True)
    record_audio = models.BooleanField(default=True)
    
    # File paths
    video_file_path = models.CharField(max_length=500, blank=True)
    audio_file_path = models.CharField(max_length=500, blank=True)
    thumbnail_path = models.CharField(max_length=500, blank=True)
    
    # File information
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    video_quality = models.CharField(max_length=20, default='720p')
    frame_rate = models.IntegerField(default=30)
    
    # Streaming information
    stream_url = models.URLField(blank=True)
    stream_key = models.CharField(max_length=100, blank=True)
    
    # Access control
    is_private = models.BooleanField(default=True)
    access_code = models.CharField(max_length=20, blank=True)
    allowed_viewers = models.ManyToManyField(HMSUser, blank=True, related_name='allowed_webcam_sessions')
    
    # Session metadata
    participant_count = models.IntegerField(default=0)
    max_participants = models.IntegerField(default=2)
    
    # Notes and comments
    session_notes = models.TextField(blank=True)
    technical_notes = models.TextField(blank=True)
    
    # Quality metrics
    connection_quality = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], blank=True)
    
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_webcam_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Webcam Session'
        verbose_name_plural = 'Webcam Sessions'
    
    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = f"WS{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate duration if both start and end times are available
        if self.actual_start and self.actual_end:
            self.duration = self.actual_end - self.actual_start
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.session_id} - {self.session_name or 'Unnamed Session'}"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_completed(self):
        return self.status == 'completed'


class WebcamRecording(models.Model):
    """Webcam recording files and metadata"""
    RECORDING_TYPE_CHOICES = [
        ('session', 'Session Recording'),
        ('scheduled', 'Scheduled Recording'),
        ('motion', 'Motion Detection'),
        ('manual', 'Manual Recording'),
    ]
    
    STATUS_CHOICES = [
        ('recording', 'Recording'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    
    recording_id = models.CharField(max_length=20, unique=True, blank=True)
    session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, null=True, blank=True, related_name='recordings')
    webcam_device = models.ForeignKey(WebcamDevice, on_delete=models.CASCADE, related_name='recordings')
    
    recording_type = models.CharField(max_length=20, choices=RECORDING_TYPE_CHOICES, default='session')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recording')
    
    # Recording details
    recording_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # File information
    file_path = models.CharField(max_length=500, blank=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    file_format = models.CharField(max_length=20, default='mp4')
    
    # Video specifications
    resolution = models.CharField(max_length=50, blank=True)
    frame_rate = models.IntegerField(default=30)
    bitrate = models.IntegerField(default=1000)
    
    # Audio specifications
    has_audio = models.BooleanField(default=True)
    audio_format = models.CharField(max_length=20, blank=True)
    audio_bitrate = models.IntegerField(default=128)
    
    # Thumbnail and preview
    thumbnail_path = models.CharField(max_length=500, blank=True)
    preview_path = models.CharField(max_length=500, blank=True)
    
    # Metadata
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True)
    
    # Access control
    is_confidential = models.BooleanField(default=True)
    retention_period_days = models.IntegerField(default=365)
    auto_delete_date = models.DateTimeField(null=True, blank=True)
    
    # Tags and categories
    tags = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    # Privacy and consent
    consent_obtained = models.BooleanField(default=False)
    consent_document = models.CharField(max_length=500, blank=True)
    
    # Processing information
    processing_started = models.DateTimeField(null=True, blank=True)
    processing_completed = models.DateTimeField(null=True, blank=True)
    processing_error = models.TextField(blank=True)
    
    # Archive information
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    archive_location = models.CharField(max_length=500, blank=True)
    
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_recordings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Webcam Recording'
        verbose_name_plural = 'Webcam Recordings'
    
    def save(self, *args, **kwargs):
        if not self.recording_id:
            self.recording_id = f"REC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate duration if both start and end times are available
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        
        # Set auto delete date based on retention period
        if self.retention_period_days and not self.auto_delete_date:
            self.auto_delete_date = self.start_time + timezone.timedelta(days=self.retention_period_days)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.recording_id} - {self.recording_name or 'Unnamed Recording'}"
    
    @property
    def is_expired(self):
        return self.auto_delete_date and timezone.now() > self.auto_delete_date


class WebcamAlert(models.Model):
    """Webcam system alerts and notifications"""
    ALERT_TYPE_CHOICES = [
        ('device_offline', 'Device Offline'),
        ('motion_detected', 'Motion Detected'),
        ('recording_failed', 'Recording Failed'),
        ('storage_full', 'Storage Full'),
        ('maintenance_due', 'Maintenance Due'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('connection_lost', 'Connection Lost'),
        ('quality_degraded', 'Quality Degraded'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    alert_id = models.CharField(max_length=20, unique=True, blank=True)
    webcam_device = models.ForeignKey(WebcamDevice, on_delete=models.CASCADE, related_name='alerts')
    
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Alert details
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Timestamps
    occurred_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Personnel
    acknowledged_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_alerts')
    resolved_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')
    
    # Actions taken
    action_taken = models.TextField(blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Notification settings
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-occurred_at']
        verbose_name = 'Webcam Alert'
        verbose_name_plural = 'Webcam Alerts'
    
    def save(self, *args, **kwargs):
        if not self.alert_id:
            self.alert_id = f"ALT{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.alert_id} - {self.title}"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_resolved(self):
        return self.status == 'resolved'


class WebcamSettings(models.Model):
    """System-wide webcam settings"""
    # Storage settings
    default_storage_path = models.CharField(max_length=500, default='/media/webcam/')
    max_storage_gb = models.IntegerField(default=100)
    auto_cleanup_enabled = models.BooleanField(default=True)
    
    # Recording settings
    default_recording_format = models.CharField(max_length=20, default='mp4')
    default_video_quality = models.CharField(max_length=20, default='720p')
    default_frame_rate = models.IntegerField(default=30)
    
    # Streaming settings
    max_concurrent_streams = models.IntegerField(default=10)
    stream_buffer_size = models.IntegerField(default=1024)
    
    # Security settings
    require_authentication = models.BooleanField(default=True)
    session_timeout_minutes = models.IntegerField(default=60)
    max_failed_attempts = models.IntegerField(default=3)
    
    # Notification settings
    alert_email_enabled = models.BooleanField(default=True)
    alert_sms_enabled = models.BooleanField(default=False)
    maintenance_reminder_days = models.IntegerField(default=30)
    
    # Performance settings
    max_resolution = models.CharField(max_length=50, default='1920x1080')
    compression_level = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # Privacy settings
    default_retention_days = models.IntegerField(default=365)
    require_consent = models.BooleanField(default=True)
    watermark_enabled = models.BooleanField(default=True)
    watermark_text = models.CharField(max_length=200, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Webcam Settings'
        verbose_name_plural = 'Webcam Settings'
    
    def __str__(self):
        return f"Webcam Settings - {self.created_at.date()}" 