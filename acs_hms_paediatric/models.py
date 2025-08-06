from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from acs_hms_base.models import Patient, HMSUser, Appointment, MedicalRecord


class PediatricPatient(models.Model):
    """Extended Patient Model for Pediatrics"""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='pediatric_profile')
    
    # Birth Information
    birth_weight = models.FloatField(blank=True, null=True, verbose_name="Birth Weight (grams)")
    birth_height = models.FloatField(blank=True, null=True, verbose_name="Birth Height (cm)")
    birth_head_circumference = models.FloatField(blank=True, null=True, verbose_name="Birth Head Circumference (cm)")
    gestational_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Gestational Age (weeks)")
    
    DELIVERY_TYPE_CHOICES = [
        ('NORMAL', 'Normal Vaginal Delivery'),
        ('CESAREAN', 'Cesarean Section'),
        ('FORCEPS', 'Forceps Delivery'),
        ('VACUUM', 'Vacuum Extraction'),
    ]
    
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, blank=True, null=True, verbose_name="Delivery Type")
    apgar_score_1_min = models.PositiveIntegerField(blank=True, null=True, verbose_name="APGAR Score (1 min)")
    apgar_score_5_min = models.PositiveIntegerField(blank=True, null=True, verbose_name="APGAR Score (5 min)")
    
    # Feeding History
    FEEDING_TYPE_CHOICES = [
        ('BREASTFED', 'Exclusively Breastfed'),
        ('FORMULA', 'Formula Fed'),
        ('MIXED', 'Mixed Feeding'),
        ('SOLID', 'Solid Food'),
    ]
    
    current_feeding_type = models.CharField(max_length=20, choices=FEEDING_TYPE_CHOICES, blank=True, null=True, verbose_name="Current Feeding Type")
    breastfeeding_duration = models.PositiveIntegerField(blank=True, null=True, verbose_name="Breastfeeding Duration (months)")
    solid_food_start_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Solid Food Start Age (months)")
    
    # Developmental Milestones
    head_control_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Head Control Age (months)")
    sitting_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Sitting Age (months)")
    crawling_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Crawling Age (months)")
    walking_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Walking Age (months)")
    first_word_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="First Word Age (months)")
    
    # School Information
    school_attending = models.BooleanField(default=False, verbose_name="Attending School")
    school_grade = models.CharField(max_length=50, blank=True, null=True, verbose_name="School Grade")
    learning_difficulties = models.BooleanField(default=False, verbose_name="Learning Difficulties")
    
    # Social History
    parents_marital_status = models.CharField(max_length=20, blank=True, null=True, verbose_name="Parents Marital Status")
    siblings_count = models.PositiveIntegerField(default=0, verbose_name="Number of Siblings")
    family_structure = models.TextField(blank=True, null=True, verbose_name="Family Structure")
    
    # Previous Medical History
    previous_hospitalizations = models.TextField(blank=True, null=True, verbose_name="Previous Hospitalizations")
    chronic_conditions = models.TextField(blank=True, null=True, verbose_name="Chronic Conditions")
    
    class Meta:
        verbose_name = "Pediatric Patient"
        verbose_name_plural = "Pediatric Patients"
    
    def __str__(self):
        return f"Pediatric Profile - {self.patient.full_name}"
    
    @property
    def age_in_months(self):
        """Calculate age in months"""
        today = date.today()
        birth_date = self.patient.date_of_birth
        return (today.year - birth_date.year) * 12 + (today.month - birth_date.month)


class GrowthChart(models.Model):
    """Growth Chart Tracking"""
    patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='growth_charts')
    measurement_date = models.DateField(verbose_name="Measurement Date")
    age_in_months = models.PositiveIntegerField(verbose_name="Age in Months")
    
    # Physical Measurements
    weight = models.FloatField(verbose_name="Weight (kg)")
    height = models.FloatField(verbose_name="Height (cm)")
    head_circumference = models.FloatField(blank=True, null=True, verbose_name="Head Circumference (cm)")
    
    # Growth Percentiles
    weight_percentile = models.FloatField(blank=True, null=True, verbose_name="Weight Percentile")
    height_percentile = models.FloatField(blank=True, null=True, verbose_name="Height Percentile")
    head_circumference_percentile = models.FloatField(blank=True, null=True, verbose_name="Head Circumference Percentile")
    bmi = models.FloatField(blank=True, null=True, verbose_name="BMI")
    bmi_percentile = models.FloatField(blank=True, null=True, verbose_name="BMI Percentile")
    
    # Assessment
    NUTRITIONAL_STATUS_CHOICES = [
        ('NORMAL', 'Normal'),
        ('UNDERWEIGHT', 'Underweight'),
        ('OVERWEIGHT', 'Overweight'),
        ('OBESE', 'Obese'),
        ('STUNTED', 'Stunted'),
        ('WASTED', 'Wasted'),
    ]
    
    nutritional_status = models.CharField(max_length=20, choices=NUTRITIONAL_STATUS_CHOICES, blank=True, null=True, verbose_name="Nutritional Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Growth Chart"
        verbose_name_plural = "Growth Charts"
        ordering = ['-measurement_date']
    
    def __str__(self):
        return f"Growth Chart - {self.patient.patient.full_name} ({self.measurement_date})"


class VaccinationRecord(models.Model):
    """Vaccination and Immunization Records"""
    patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='vaccination_records')
    
    VACCINE_TYPE_CHOICES = [
        ('BCG', 'BCG'),
        ('HEPATITIS_B', 'Hepatitis B'),
        ('POLIO_OPV', 'Polio (OPV)'),
        ('POLIO_IPV', 'Polio (IPV)'),
        ('DTP', 'DTP'),
        ('PENTAVALENT', 'Pentavalent'),
        ('HIB', 'Haemophilus influenzae type b'),
        ('PNEUMOCOCCAL', 'Pneumococcal'),
        ('ROTAVIRUS', 'Rotavirus'),
        ('MEASLES', 'Measles'),
        ('MMR', 'MMR'),
        ('VARICELLA', 'Varicella'),
        ('HEPATITIS_A', 'Hepatitis A'),
        ('TYPHOID', 'Typhoid'),
        ('MENINGOCOCCAL', 'Meningococcal'),
        ('HPV', 'HPV'),
        ('INFLUENZA', 'Influenza'),
        ('COVID19', 'COVID-19'),
    ]
    
    vaccine_type = models.CharField(max_length=20, choices=VACCINE_TYPE_CHOICES, verbose_name="Vaccine Type")
    dose_number = models.PositiveIntegerField(verbose_name="Dose Number")
    vaccination_date = models.DateField(verbose_name="Vaccination Date")
    age_given = models.PositiveIntegerField(verbose_name="Age Given (months)")
    
    # Vaccine Details
    vaccine_brand = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vaccine Brand")
    batch_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Batch Number")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Expiry Date")
    
    # Administration Details
    administered_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='administered_vaccines')
    site_of_injection = models.CharField(max_length=50, blank=True, null=True, verbose_name="Site of Injection")
    
    # Adverse Events
    adverse_events = models.TextField(blank=True, null=True, verbose_name="Adverse Events")
    
    # Next Dose
    next_dose_due = models.DateField(blank=True, null=True, verbose_name="Next Dose Due")
    
    class Meta:
        verbose_name = "Vaccination Record"
        verbose_name_plural = "Vaccination Records"
        ordering = ['-vaccination_date']
        unique_together = ['patient', 'vaccine_type', 'dose_number']
    
    def __str__(self):
        return f"{self.get_vaccine_type_display()} Dose {self.dose_number} - {self.patient.patient.full_name}"


class DevelopmentalAssessment(models.Model):
    """Developmental Assessment"""
    patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='developmental_assessments')
    assessment_date = models.DateField(verbose_name="Assessment Date")
    age_in_months = models.PositiveIntegerField(verbose_name="Age in Months")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='developmental_assessments')
    
    # Motor Development
    gross_motor_skills = models.TextField(blank=True, null=True, verbose_name="Gross Motor Skills")
    fine_motor_skills = models.TextField(blank=True, null=True, verbose_name="Fine Motor Skills")
    
    # Language Development
    receptive_language = models.TextField(blank=True, null=True, verbose_name="Receptive Language")
    expressive_language = models.TextField(blank=True, null=True, verbose_name="Expressive Language")
    
    # Social Development
    social_skills = models.TextField(blank=True, null=True, verbose_name="Social Skills")
    emotional_development = models.TextField(blank=True, null=True, verbose_name="Emotional Development")
    
    # Cognitive Development
    cognitive_skills = models.TextField(blank=True, null=True, verbose_name="Cognitive Skills")
    problem_solving = models.TextField(blank=True, null=True, verbose_name="Problem Solving")
    
    # Assessment Tools Used
    assessment_tools = models.TextField(blank=True, null=True, verbose_name="Assessment Tools Used")
    
    # Overall Assessment
    DEVELOPMENT_STATUS_CHOICES = [
        ('NORMAL', 'Normal Development'),
        ('DELAYED', 'Delayed Development'),
        ('ADVANCED', 'Advanced Development'),
        ('MIXED', 'Mixed Development'),
    ]
    
    development_status = models.CharField(max_length=20, choices=DEVELOPMENT_STATUS_CHOICES, verbose_name="Development Status")
    concerns = models.TextField(blank=True, null=True, verbose_name="Concerns")
    recommendations = models.TextField(blank=True, null=True, verbose_name="Recommendations")
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False, verbose_name="Follow-up Required")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    class Meta:
        verbose_name = "Developmental Assessment"
        verbose_name_plural = "Developmental Assessments"
        ordering = ['-assessment_date']
    
    def __str__(self):
        return f"Developmental Assessment - {self.patient.patient.full_name} ({self.assessment_date})"


class PediatricMedicalRecord(models.Model):
    """Specialized Medical Record for Pediatrics"""
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, related_name='pediatric_record')
    pediatric_patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='medical_records')
    
    # Child-Specific History
    birth_history = models.TextField(blank=True, null=True, verbose_name="Birth History")
    feeding_history = models.TextField(blank=True, null=True, verbose_name="Feeding History")
    developmental_history = models.TextField(blank=True, null=True, verbose_name="Developmental History")
    immunization_status = models.TextField(blank=True, null=True, verbose_name="Immunization Status")
    
    # Growth Parameters
    weight_for_age = models.CharField(max_length=20, blank=True, null=True, verbose_name="Weight for Age")
    height_for_age = models.CharField(max_length=20, blank=True, null=True, verbose_name="Height for Age")
    head_circumference_for_age = models.CharField(max_length=20, blank=True, null=True, verbose_name="Head Circumference for Age")
    
    # Behavioral Assessment
    behavior_concerns = models.TextField(blank=True, null=True, verbose_name="Behavior Concerns")
    sleep_patterns = models.TextField(blank=True, null=True, verbose_name="Sleep Patterns")
    eating_patterns = models.TextField(blank=True, null=True, verbose_name="Eating Patterns")
    
    # School Performance
    school_performance = models.TextField(blank=True, null=True, verbose_name="School Performance")
    
    # Parent/Guardian Information
    caregiver_concerns = models.TextField(blank=True, null=True, verbose_name="Caregiver Concerns")
    family_dynamics = models.TextField(blank=True, null=True, verbose_name="Family Dynamics")
    
    # Pediatric-Specific Treatment
    age_appropriate_treatment = models.TextField(blank=True, null=True, verbose_name="Age-Appropriate Treatment")
    medication_dosing = models.TextField(blank=True, null=True, verbose_name="Medication Dosing")
    parent_education = models.TextField(blank=True, null=True, verbose_name="Parent Education")
    
    class Meta:
        verbose_name = "Pediatric Medical Record"
        verbose_name_plural = "Pediatric Medical Records"
    
    def __str__(self):
        return f"Pediatric Record - {self.pediatric_patient.patient.full_name}"


class NutritionalAssessment(models.Model):
    """Nutritional Assessment for Children"""
    patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='nutritional_assessments')
    assessment_date = models.DateField(verbose_name="Assessment Date")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nutritional_assessments')
    
    # Dietary History
    feeding_pattern = models.TextField(verbose_name="Feeding Pattern")
    food_preferences = models.TextField(blank=True, null=True, verbose_name="Food Preferences")
    food_allergies = models.TextField(blank=True, null=True, verbose_name="Food Allergies")
    vitamin_supplements = models.TextField(blank=True, null=True, verbose_name="Vitamin Supplements")
    
    # Anthropometric Assessment
    weight_for_height = models.CharField(max_length=20, blank=True, null=True, verbose_name="Weight for Height")
    mid_upper_arm_circumference = models.FloatField(blank=True, null=True, verbose_name="Mid Upper Arm Circumference (cm)")
    tricep_skinfold = models.FloatField(blank=True, null=True, verbose_name="Tricep Skinfold (mm)")
    
    # Clinical Assessment
    NUTRITIONAL_STATUS_CHOICES = [
        ('NORMAL', 'Normal'),
        ('MILD_MALNUTRITION', 'Mild Malnutrition'),
        ('MODERATE_MALNUTRITION', 'Moderate Malnutrition'),
        ('SEVERE_MALNUTRITION', 'Severe Malnutrition'),
        ('OVERWEIGHT', 'Overweight'),
        ('OBESE', 'Obese'),
    ]
    
    nutritional_status = models.CharField(max_length=30, choices=NUTRITIONAL_STATUS_CHOICES, verbose_name="Nutritional Status")
    clinical_signs = models.TextField(blank=True, null=True, verbose_name="Clinical Signs")
    
    # Laboratory Results
    hemoglobin = models.FloatField(blank=True, null=True, verbose_name="Hemoglobin (g/dL)")
    serum_albumin = models.FloatField(blank=True, null=True, verbose_name="Serum Albumin (g/dL)")
    vitamin_d = models.FloatField(blank=True, null=True, verbose_name="Vitamin D (ng/mL)")
    
    # Recommendations
    dietary_recommendations = models.TextField(blank=True, null=True, verbose_name="Dietary Recommendations")
    supplement_recommendations = models.TextField(blank=True, null=True, verbose_name="Supplement Recommendations")
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    class Meta:
        verbose_name = "Nutritional Assessment"
        verbose_name_plural = "Nutritional Assessments"
        ordering = ['-assessment_date']
    
    def __str__(self):
        return f"Nutritional Assessment - {self.patient.patient.full_name} ({self.assessment_date})"


class PediatricProcedure(models.Model):
    """Pediatric Procedures"""
    PROCEDURE_TYPE_CHOICES = [
        ('CIRCUMCISION', 'Circumcision'),
        ('HERNIA_REPAIR', 'Hernia Repair'),
        ('LUMBAR_PUNCTURE', 'Lumbar Puncture'),
        ('BONE_MARROW_ASPIRATION', 'Bone Marrow Aspiration'),
        ('FOREIGN_BODY_REMOVAL', 'Foreign Body Removal'),
        ('TONSILLECTOMY', 'Tonsillectomy'),
        ('ADENOIDECTOMY', 'Adenoidectomy'),
        ('APPENDECTOMY', 'Appendectomy'),
        ('CARDIAC_CATHETERIZATION', 'Cardiac Catheterization'),
        ('ENDOSCOPY', 'Endoscopy'),
        ('BRONCHOSCOPY', 'Bronchoscopy'),
        ('CENTRAL_LINE_INSERTION', 'Central Line Insertion'),
    ]
    
    patient = models.ForeignKey(PediatricPatient, on_delete=models.CASCADE, related_name='procedures')
    procedure_type = models.CharField(max_length=50, choices=PROCEDURE_TYPE_CHOICES, verbose_name="Procedure Type")
    procedure_date = models.DateField(verbose_name="Procedure Date")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='pediatric_procedures')
    
    # Pre-procedure
    pre_procedure_weight = models.FloatField(blank=True, null=True, verbose_name="Pre-procedure Weight (kg)")
    pre_procedure_assessment = models.TextField(blank=True, null=True, verbose_name="Pre-procedure Assessment")
    consent_obtained = models.BooleanField(default=False, verbose_name="Consent Obtained")
    
    # Procedure Details
    procedure_details = models.TextField(blank=True, null=True, verbose_name="Procedure Details")
    anesthesia_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Anesthesia Type")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Post-procedure
    post_procedure_care = models.TextField(blank=True, null=True, verbose_name="Post-procedure Care")
    parent_instructions = models.TextField(blank=True, null=True, verbose_name="Parent Instructions")
    
    # Follow-up
    follow_up_required = models.BooleanField(default=True, verbose_name="Follow-up Required")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    class Meta:
        verbose_name = "Pediatric Procedure"
        verbose_name_plural = "Pediatric Procedures"
        ordering = ['-procedure_date']
    
    def __str__(self):
        return f"{self.get_procedure_type_display()} - {self.patient.patient.full_name} ({self.procedure_date})" 