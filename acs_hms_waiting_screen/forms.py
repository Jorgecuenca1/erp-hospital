from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import (
    WaitingScreen, WaitingQueue, ScreenAnnouncement, HealthTip, ScreenConfiguration
)


class WaitingScreenForm(forms.ModelForm):
    class Meta:
        model = WaitingScreen
        fields = '__all__'
        widgets = {
            'theme_color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('screen_type', css_class='form-group col-md-6'),
            ),
            'location',
            Row(
                Column('display_queue', css_class='form-group col-md-3'),
                Column('display_announcements', css_class='form-group col-md-3'),
                Column('display_health_tips', css_class='form-group col-md-3'),
                Column('display_weather', css_class='form-group col-md-3'),
            ),
            Row(
                Column('refresh_interval', css_class='form-group col-md-6'),
                Column('theme_color', css_class='form-group col-md-6'),
            ),
            'logo_file',
            'is_active',
            Submit('submit', 'Save Waiting Screen', css_class='btn btn-primary')
        )


class WaitingQueueForm(forms.ModelForm):
    class Meta:
        model = WaitingQueue
        fields = '__all__'
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'called_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('queue_number', css_class='form-group col-md-6'),
                Column('patient', css_class='form-group col-md-6'),
            ),
            Row(
                Column('doctor', css_class='form-group col-md-6'),
                Column('screen', css_class='form-group col-md-6'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6'),
                Column('estimated_wait_minutes', css_class='form-group col-md-6'),
            ),
            'notes',
            Submit('submit', 'Save Queue Entry', css_class='btn btn-primary')
        )


class ScreenAnnouncementForm(forms.ModelForm):
    class Meta:
        model = ScreenAnnouncement
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-8'),
                Column('announcement_type', css_class='form-group col-md-4'),
            ),
            'content',
            Row(
                Column('priority', css_class='form-group col-md-6'),
                Column('is_active', css_class='form-group col-md-6'),
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6'),
                Column('end_date', css_class='form-group col-md-6'),
            ),
            'screens',
            Submit('submit', 'Save Announcement', css_class='btn btn-primary')
        )


class HealthTipForm(forms.ModelForm):
    class Meta:
        model = HealthTip
        fields = ['title', 'content', 'category', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-8'),
                Column('category', css_class='form-group col-md-4'),
            ),
            'content',
            'is_active',
            Submit('submit', 'Save Health Tip', css_class='btn btn-primary')
        )


class ScreenConfigurationForm(forms.ModelForm):
    class Meta:
        model = ScreenConfiguration
        fields = '__all__'
        widgets = {
            'default_theme_color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('default_refresh_interval', css_class='form-group col-md-6'),
                Column('default_theme_color', css_class='form-group col-md-6'),
            ),
            Row(
                Column('show_queue_numbers', css_class='form-group col-md-4'),
                Column('show_wait_times', css_class='form-group col-md-4'),
                Column('show_doctor_names', css_class='form-group col-md-4'),
            ),
            Row(
                Column('enable_audio_announcements', css_class='form-group col-md-6'),
                Column('audio_language', css_class='form-group col-md-6'),
            ),
            'health_tips_interval',
            Submit('submit', 'Save Configuration', css_class='btn btn-primary')
        )


class WaitingScreenSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search screens...', 'class': 'form-control'})
    )
    screen_type = forms.ChoiceField(
        choices=[('', 'All Types')] + WaitingScreen.SCREEN_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('search', css_class='form-group col-md-4'),
                Column('screen_type', css_class='form-group col-md-4'),
                Column('is_active', css_class='form-group col-md-4'),
            ),
            Submit('submit', 'Search', css_class='btn btn-primary')
        ) 