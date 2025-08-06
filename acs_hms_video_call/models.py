from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
from acs_hms_online_appointment.models import OnlineAppointment
import uuid


class VideoCallPlatform(models.Model):
    """Video call platform configurations"""
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'),
        ('teams', 'Microsoft Teams'),
        ('meet', 'Google Meet'),
        ('webex', 'Cisco Webex'),
        ('jitsi', 'Jitsi Meet'),
        ('agora', 'Agora'),
        ('twilio', 'Twilio Video'),
        ('custom', 'Custom Platform'),
    ]
    
    name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    
    # API Configuration
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    webhook_url = models.URLField(blank=True)
    
    # Platform specific settings
    base_url = models.URLField(blank=True)
    sdk_version = models.CharField(max_length=50, blank=True)
    
    # Features
    max_participants = models.IntegerField(default=10)
    recording_enabled = models.BooleanField(default=True)
    screen_sharing_enabled = models.BooleanField(default=True)
    chat_enabled = models.BooleanField(default=True)
    waiting_room_enabled = models.BooleanField(default=True)
    
    # Security
    password_required = models.BooleanField(default=True)
    encryption_enabled = models.BooleanField(default=True)
    
    # Limits
    max_duration_minutes = models.IntegerField(default=60)
    concurrent_meetings_limit = models.IntegerField(default=10)
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Video Call Platform'
        verbose_name_plural = 'Video Call Platforms'
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"


class VideoCallRoom(models.Model):
    """Video call rooms for telemedicine"""
    ROOM_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('group_therapy', 'Group Therapy'),
        ('conference', 'Conference'),
        ('training', 'Training'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('disabled', 'Disabled'),
    ]
    
    room_id = models.CharField(max_length=20, unique=True, blank=True)
    room_name = models.CharField(max_length=200)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='consultation')
    
    platform = models.ForeignKey(VideoCallPlatform, on_delete=models.CASCADE, related_name='rooms')
    
    # Room configuration
    max_participants = models.IntegerField(default=2)
    waiting_room_enabled = models.BooleanField(default=True)
    password_required = models.BooleanField(default=True)
    recording_enabled = models.BooleanField(default=True)
    
    # Access settings
    room_password = models.CharField(max_length=50, blank=True)
    join_url = models.URLField(blank=True)
    moderator_url = models.URLField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_participants = models.IntegerField(default=0)
    
    # Assignment
    assigned_doctor = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_rooms')
    department = models.CharField(max_length=100, blank=True)
    
    # Settings
    auto_record = models.BooleanField(default=False)
    allow_screen_sharing = models.BooleanField(default=True)
    allow_chat = models.BooleanField(default=True)
    
    # Maintenance
    last_used = models.DateTimeField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['room_name']
        verbose_name = 'Video Call Room'
        verbose_name_plural = 'Video Call Rooms'
    
    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = f"VR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.room_name} ({self.room_id})"
    
    @property
    def is_available(self):
        return self.status == 'available' and self.current_participants < self.max_participants


class VideoCall(models.Model):
    """Video call sessions"""
    CALL_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('second_opinion', 'Second Opinion'),
        ('group_consultation', 'Group Consultation'),
        ('therapy_session', 'Therapy Session'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
        ('no_show', 'No Show'),
    ]
    
    call_id = models.CharField(max_length=20, unique=True, blank=True)
    room = models.ForeignKey(VideoCallRoom, on_delete=models.CASCADE, related_name='calls')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='video_call')
    online_appointment = models.OneToOneField(OnlineAppointment, on_delete=models.CASCADE, null=True, blank=True, related_name='video_call')
    
    call_type = models.CharField(max_length=20, choices=CALL_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Participants
    host = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='hosted_calls')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='video_calls')
    additional_participants = models.ManyToManyField(HMSUser, blank=True, related_name='video_call_participants')
    
    # Call scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Call details
    subject = models.CharField(max_length=200, blank=True)
    agenda = models.TextField(blank=True)
    
    # Platform specific
    meeting_id = models.CharField(max_length=100, blank=True)
    meeting_password = models.CharField(max_length=50, blank=True)
    join_url = models.URLField(blank=True)
    host_url = models.URLField(blank=True)
    
    # Recording
    is_recorded = models.BooleanField(default=False)
    recording_url = models.URLField(blank=True)
    recording_password = models.CharField(max_length=50, blank=True)
    recording_file_path = models.CharField(max_length=500, blank=True)
    
    # Quality metrics
    audio_quality = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], blank=True)
    video_quality = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], blank=True)
    
    # Connection info
    participant_count = models.IntegerField(default=0)
    max_participants_reached = models.IntegerField(default=0)
    
    # Technical details
    platform_response = models.JSONField(default=dict, blank=True)
    connection_logs = models.JSONField(default=list, blank=True)
    
    # Call outcome
    consultation_notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    # Cancellation
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_calls')
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Notifications
    reminder_sent = models.BooleanField(default=False)
    follow_up_sent = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_calls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_start']
        verbose_name = 'Video Call'
        verbose_name_plural = 'Video Calls'
    
    def save(self, *args, **kwargs):
        if not self.call_id:
            self.call_id = f"VC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate duration if both start and end times are available
        if self.actual_start and self.actual_end:
            self.duration = self.actual_end - self.actual_start
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.call_id} - {self.patient.name} - {self.host.user.get_full_name()}"
    
    @property
    def is_active(self):
        return self.status == 'in_progress'
    
    @property
    def is_upcoming(self):
        return self.status == 'scheduled' and self.scheduled_start > timezone.now()


class VideoCallParticipant(models.Model):
    """Individual participant data for video calls"""
    PARTICIPANT_TYPE_CHOICES = [
        ('host', 'Host'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('observer', 'Observer'),
        ('interpreter', 'Interpreter'),
        ('family', 'Family Member'),
    ]
    
    STATUS_CHOICES = [
        ('invited', 'Invited'),
        ('joined', 'Joined'),
        ('left', 'Left'),
        ('removed', 'Removed'),
        ('rejected', 'Rejected'),
    ]
    
    call = models.ForeignKey(VideoCall, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hms_user = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True)
    
    participant_type = models.CharField(max_length=20, choices=PARTICIPANT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='invited')
    
    # Participant details
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Join details
    join_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Technical details
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Permissions
    can_share_screen = models.BooleanField(default=True)
    can_use_chat = models.BooleanField(default=True)
    can_use_audio = models.BooleanField(default=True)
    can_use_video = models.BooleanField(default=True)
    
    # Activity
    spoke_duration = models.DurationField(null=True, blank=True)
    chat_messages_sent = models.IntegerField(default=0)
    
    # Connection quality
    avg_connection_quality = models.CharField(max_length=20, blank=True)
    connection_issues = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['join_time']
        verbose_name = 'Video Call Participant'
        verbose_name_plural = 'Video Call Participants'
    
    def save(self, *args, **kwargs):
        # Calculate duration if both join and leave times are available
        if self.join_time and self.leave_time:
            self.duration = self.leave_time - self.join_time
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.call.call_id} - {self.name or self.user.get_full_name()}"


class VideoCallRecording(models.Model):
    """Video call recordings"""
    RECORDING_TYPE_CHOICES = [
        ('cloud', 'Cloud Recording'),
        ('local', 'Local Recording'),
        ('hybrid', 'Hybrid Recording'),
    ]
    
    STATUS_CHOICES = [
        ('recording', 'Recording'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ]
    
    recording_id = models.CharField(max_length=20, unique=True, blank=True)
    call = models.ForeignKey(VideoCall, on_delete=models.CASCADE, related_name='recordings')
    
    recording_type = models.CharField(max_length=20, choices=RECORDING_TYPE_CHOICES, default='cloud')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recording')
    
    # Recording details
    recording_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # File information
    file_path = models.CharField(max_length=500, blank=True)
    file_url = models.URLField(blank=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Recording specifications
    resolution = models.CharField(max_length=20, default='720p')
    frame_rate = models.IntegerField(default=30)
    audio_quality = models.CharField(max_length=20, default='standard')
    
    # Timing
    recording_start = models.DateTimeField()
    recording_end = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Platform specific
    platform_recording_id = models.CharField(max_length=100, blank=True)
    download_url = models.URLField(blank=True)
    playback_url = models.URLField(blank=True)
    password = models.CharField(max_length=50, blank=True)
    
    # Access control
    is_public = models.BooleanField(default=False)
    allowed_viewers = models.ManyToManyField(HMSUser, blank=True, related_name='allowed_recordings')
    
    # Retention
    retention_period_days = models.IntegerField(default=365)
    auto_delete_date = models.DateTimeField(null=True, blank=True)
    
    # Privacy
    consent_obtained = models.BooleanField(default=False)
    consent_document = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recording_start']
        verbose_name = 'Video Call Recording'
        verbose_name_plural = 'Video Call Recordings'
    
    def save(self, *args, **kwargs):
        if not self.recording_id:
            self.recording_id = f"VCR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate duration if both start and end times are available
        if self.recording_start and self.recording_end:
            self.duration = self.recording_end - self.recording_start
        
        # Set auto delete date based on retention period
        if self.retention_period_days and not self.auto_delete_date:
            self.auto_delete_date = self.recording_start + timezone.timedelta(days=self.retention_period_days)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.recording_id} - {self.call.call_id}"
    
    @property
    def is_ready(self):
        return self.status == 'ready'
    
    @property
    def is_expired(self):
        return self.auto_delete_date and timezone.now() > self.auto_delete_date


class VideoCallSettings(models.Model):
    """System-wide video call settings"""
    # Default platform
    default_platform = models.ForeignKey(VideoCallPlatform, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Call settings
    default_call_duration = models.IntegerField(default=30)
    max_call_duration = models.IntegerField(default=120)
    waiting_room_timeout = models.IntegerField(default=10)
    
    # Recording settings
    auto_record_calls = models.BooleanField(default=False)
    recording_retention_days = models.IntegerField(default=365)
    require_recording_consent = models.BooleanField(default=True)
    
    # Notification settings
    send_call_reminders = models.BooleanField(default=True)
    reminder_time_minutes = models.IntegerField(default=15)
    send_follow_up_emails = models.BooleanField(default=True)
    
    # Security settings
    require_waiting_room = models.BooleanField(default=True)
    require_passwords = models.BooleanField(default=True)
    max_failed_attempts = models.IntegerField(default=3)
    
    # Quality settings
    default_video_quality = models.CharField(max_length=20, default='720p')
    bandwidth_optimization = models.BooleanField(default=True)
    
    # Integration settings
    calendar_integration = models.BooleanField(default=True)
    sms_integration = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Video Call Settings'
        verbose_name_plural = 'Video Call Settings'
    
    def __str__(self):
        return f"Video Call Settings - {self.created_at.date()}" 