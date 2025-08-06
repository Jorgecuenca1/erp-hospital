from django.db import models
from django.utils import timezone
from acs_hms_base.models import Patient, HMSUser, Appointment, MedicalRecord


class GynecologyPatient(models.Model):
    """Extended Patient Model for Gynecology"""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='gynecology_profile')
    
    # Gynecological History
    menarche_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Age at Menarche")
    menopause_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Age at Menopause")
    
    # Menstrual History
    MENSTRUAL_CYCLE_CHOICES = [
        ('REGULAR', 'Regular'),
        ('IRREGULAR', 'Irregular'),
        ('AMENORRHEA', 'Amenorrhea'),
        ('MENORRHAGIA', 'Menorrhagia'),
        ('OLIGOMENORRHEA', 'Oligomenorrhea'),
    ]
    
    menstrual_cycle = models.CharField(max_length=20, choices=MENSTRUAL_CYCLE_CHOICES, blank=True, null=True, verbose_name="Menstrual Cycle")
    cycle_length = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cycle Length (days)")
    flow_duration = models.PositiveIntegerField(blank=True, null=True, verbose_name="Flow Duration (days)")
    last_menstrual_period = models.DateField(blank=True, null=True, verbose_name="Last Menstrual Period")
    
    # Obstetric History
    gravida = models.PositiveIntegerField(default=0, verbose_name="Gravida (G)")
    para = models.PositiveIntegerField(default=0, verbose_name="Para (P)")
    term_deliveries = models.PositiveIntegerField(default=0, verbose_name="Term Deliveries")
    preterm_deliveries = models.PositiveIntegerField(default=0, verbose_name="Preterm Deliveries")
    abortions = models.PositiveIntegerField(default=0, verbose_name="Abortions")
    living_children = models.PositiveIntegerField(default=0, verbose_name="Living Children")
    
    # Contraceptive History
    CONTRACEPTIVE_CHOICES = [
        ('NONE', 'None'),
        ('ORAL_PILL', 'Oral Contraceptive Pill'),
        ('IUD', 'Intrauterine Device'),
        ('CONDOM', 'Condom'),
        ('INJECTION', 'Injection'),
        ('IMPLANT', 'Implant'),
        ('STERILIZATION', 'Sterilization'),
        ('NATURAL', 'Natural Methods'),
    ]
    
    current_contraceptive = models.CharField(max_length=20, choices=CONTRACEPTIVE_CHOICES, default='NONE', verbose_name="Current Contraceptive Method")
    contraceptive_duration = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contraceptive Duration")
    
    # Screening History
    last_pap_smear = models.DateField(blank=True, null=True, verbose_name="Last Pap Smear")
    pap_smear_result = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pap Smear Result")
    last_mammogram = models.DateField(blank=True, null=True, verbose_name="Last Mammogram")
    mammogram_result = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mammogram Result")
    
    # Additional Information
    surgical_history = models.TextField(blank=True, null=True, verbose_name="Gynecological Surgical History")
    family_history = models.TextField(blank=True, null=True, verbose_name="Family History (Gynecological)")
    
    class Meta:
        verbose_name = "Gynecology Patient"
        verbose_name_plural = "Gynecology Patients"
    
    def __str__(self):
        return f"Gynecology Profile - {self.patient.full_name}"


class Pregnancy(models.Model):
    """Pregnancy Management"""
    PREGNANCY_STATUS_CHOICES = [
        ('ONGOING', 'Ongoing'),
        ('DELIVERED', 'Delivered'),
        ('ABORTED', 'Aborted'),
        ('ECTOPIC', 'Ectopic'),
        ('MOLAR', 'Molar'),
    ]
    
    patient = models.ForeignKey(GynecologyPatient, on_delete=models.CASCADE, related_name='pregnancies')
    pregnancy_number = models.PositiveIntegerField(verbose_name="Pregnancy Number")
    
    # Pregnancy Dates
    last_menstrual_period = models.DateField(verbose_name="Last Menstrual Period")
    expected_delivery_date = models.DateField(verbose_name="Expected Delivery Date")
    actual_delivery_date = models.DateField(blank=True, null=True, verbose_name="Actual Delivery Date")
    
    # Pregnancy Status
    status = models.CharField(max_length=20, choices=PREGNANCY_STATUS_CHOICES, default='ONGOING', verbose_name="Pregnancy Status")
    gestational_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Gestational Age (weeks)")
    
    # High Risk Factors
    high_risk = models.BooleanField(default=False, verbose_name="High Risk Pregnancy")
    risk_factors = models.TextField(blank=True, null=True, verbose_name="Risk Factors")
    
    # Delivery Information
    DELIVERY_TYPE_CHOICES = [
        ('NORMAL', 'Normal Vaginal Delivery'),
        ('CESAREAN', 'Cesarean Section'),
        ('FORCEPS', 'Forceps Delivery'),
        ('VACUUM', 'Vacuum Extraction'),
    ]
    
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, blank=True, null=True, verbose_name="Delivery Type")
    birth_weight = models.FloatField(blank=True, null=True, verbose_name="Birth Weight (grams)")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Record Information
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    
    class Meta:
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancies"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Pregnancy {self.pregnancy_number} - {self.patient.patient.full_name}"


class AntenatalVisit(models.Model):
    """Antenatal Care Visits"""
    pregnancy = models.ForeignKey(Pregnancy, on_delete=models.CASCADE, related_name='antenatal_visits')
    visit_date = models.DateField(verbose_name="Visit Date")
    gestational_age = models.PositiveIntegerField(verbose_name="Gestational Age (weeks)")
    
    # Physical Examination
    weight = models.FloatField(blank=True, null=True, verbose_name="Weight (kg)")
    blood_pressure_systolic = models.PositiveIntegerField(blank=True, null=True, verbose_name="Blood Pressure (Systolic)")
    blood_pressure_diastolic = models.PositiveIntegerField(blank=True, null=True, verbose_name="Blood Pressure (Diastolic)")
    fundal_height = models.PositiveIntegerField(blank=True, null=True, verbose_name="Fundal Height (cm)")
    
    # Fetal Assessment
    fetal_heart_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name="Fetal Heart Rate")
    fetal_movement = models.CharField(max_length=50, blank=True, null=True, verbose_name="Fetal Movement")
    presentation = models.CharField(max_length=50, blank=True, null=True, verbose_name="Presentation")
    
    # Laboratory Results
    hemoglobin = models.FloatField(blank=True, null=True, verbose_name="Hemoglobin (g/dL)")
    urine_protein = models.CharField(max_length=10, blank=True, null=True, verbose_name="Urine Protein")
    urine_glucose = models.CharField(max_length=10, blank=True, null=True, verbose_name="Urine Glucose")
    
    # Ultrasound
    ultrasound_done = models.BooleanField(default=False, verbose_name="Ultrasound Done")
    estimated_fetal_weight = models.FloatField(blank=True, null=True, verbose_name="Estimated Fetal Weight (grams)")
    amniotic_fluid = models.CharField(max_length=50, blank=True, null=True, verbose_name="Amniotic Fluid")
    
    # Advice and Follow-up
    advice = models.TextField(blank=True, null=True, verbose_name="Advice")
    next_visit_date = models.DateField(blank=True, null=True, verbose_name="Next Visit Date")
    
    # Doctor and Notes
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='antenatal_visits', limit_choices_to={'user_type': 'DOCTOR'})
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Antenatal Visit"
        verbose_name_plural = "Antenatal Visits"
        ordering = ['-visit_date']
    
    def __str__(self):
        return f"ANC Visit - {self.pregnancy.patient.patient.full_name} ({self.visit_date})"


class GynecologyProcedure(models.Model):
    """Gynecological Procedures"""
    PROCEDURE_TYPE_CHOICES = [
        ('COLPOSCOPY', 'Colposcopy'),
        ('HYSTEROSCOPY', 'Hysteroscopy'),
        ('LAPAROSCOPY', 'Laparoscopy'),
        ('DILATION_CURETTAGE', 'Dilation & Curettage'),
        ('ENDOMETRIAL_BIOPSY', 'Endometrial Biopsy'),
        ('CERVICAL_BIOPSY', 'Cervical Biopsy'),
        ('HYSTERECTOMY', 'Hysterectomy'),
        ('MYOMECTOMY', 'Myomectomy'),
        ('OOPHORECTOMY', 'Oophorectomy'),
        ('TUBAL_LIGATION', 'Tubal Ligation'),
        ('IUD_INSERTION', 'IUD Insertion'),
        ('IUD_REMOVAL', 'IUD Removal'),
        ('LOOP_ELECTROSURGICAL_EXCISION', 'LEEP'),
        ('CRYOTHERAPY', 'Cryotherapy'),
    ]
    
    patient = models.ForeignKey(GynecologyPatient, on_delete=models.CASCADE, related_name='procedures')
    procedure_type = models.CharField(max_length=50, choices=PROCEDURE_TYPE_CHOICES, verbose_name="Procedure Type")
    procedure_date = models.DateField(verbose_name="Procedure Date")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='gynecology_procedures', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Indication
    indication = models.TextField(verbose_name="Indication")
    
    # Procedure Details
    procedure_details = models.TextField(blank=True, null=True, verbose_name="Procedure Details")
    findings = models.TextField(blank=True, null=True, verbose_name="Findings")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Anesthesia
    ANESTHESIA_TYPE_CHOICES = [
        ('LOCAL', 'Local Anesthesia'),
        ('REGIONAL', 'Regional Anesthesia'),
        ('GENERAL', 'General Anesthesia'),
        ('NONE', 'No Anesthesia'),
    ]
    
    anesthesia_type = models.CharField(max_length=20, choices=ANESTHESIA_TYPE_CHOICES, blank=True, null=True, verbose_name="Anesthesia Type")
    
    # Post-operative Care
    post_operative_instructions = models.TextField(blank=True, null=True, verbose_name="Post-operative Instructions")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    # Specimens
    specimen_sent = models.BooleanField(default=False, verbose_name="Specimen Sent for Histopathology")
    specimen_details = models.TextField(blank=True, null=True, verbose_name="Specimen Details")
    pathology_report = models.TextField(blank=True, null=True, verbose_name="Pathology Report")
    
    class Meta:
        verbose_name = "Gynecology Procedure"
        verbose_name_plural = "Gynecology Procedures"
        ordering = ['-procedure_date']
    
    def __str__(self):
        return f"{self.get_procedure_type_display()} - {self.patient.patient.full_name} ({self.procedure_date})"


class GynecologyMedicalRecord(models.Model):
    """Specialized Medical Record for Gynecology"""
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, related_name='gynecology_record')
    gynecology_patient = models.ForeignKey(GynecologyPatient, on_delete=models.CASCADE, related_name='medical_records')
    
    # Gynecological Examination
    external_genitalia = models.TextField(blank=True, null=True, verbose_name="External Genitalia")
    vaginal_examination = models.TextField(blank=True, null=True, verbose_name="Vaginal Examination")
    cervical_examination = models.TextField(blank=True, null=True, verbose_name="Cervical Examination")
    bimanual_examination = models.TextField(blank=True, null=True, verbose_name="Bimanual Examination")
    
    # Breast Examination
    breast_examination = models.TextField(blank=True, null=True, verbose_name="Breast Examination")
    
    # Specific Symptoms
    vaginal_discharge = models.TextField(blank=True, null=True, verbose_name="Vaginal Discharge")
    pelvic_pain = models.TextField(blank=True, null=True, verbose_name="Pelvic Pain")
    menstrual_irregularities = models.TextField(blank=True, null=True, verbose_name="Menstrual Irregularities")
    
    # Investigations
    ultrasound_findings = models.TextField(blank=True, null=True, verbose_name="Ultrasound Findings")
    laboratory_results = models.TextField(blank=True, null=True, verbose_name="Laboratory Results")
    
    # Gynecological Diagnosis
    gynecological_diagnosis = models.TextField(blank=True, null=True, verbose_name="Gynecological Diagnosis")
    
    # Treatment Plan
    hormonal_therapy = models.TextField(blank=True, null=True, verbose_name="Hormonal Therapy")
    surgical_plan = models.TextField(blank=True, null=True, verbose_name="Surgical Plan")
    
    class Meta:
        verbose_name = "Gynecology Medical Record"
        verbose_name_plural = "Gynecology Medical Records"
    
    def __str__(self):
        return f"Gynecology Record - {self.gynecology_patient.patient.full_name}"


class ContraceptiveConsultation(models.Model):
    """Contraceptive Counseling and Management"""
    patient = models.ForeignKey(GynecologyPatient, on_delete=models.CASCADE, related_name='contraceptive_consultations')
    consultation_date = models.DateField(verbose_name="Consultation Date")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='contraceptive_consultations', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Current Method
    current_method = models.CharField(max_length=20, choices=GynecologyPatient.CONTRACEPTIVE_CHOICES, verbose_name="Current Method")
    satisfaction_with_current = models.CharField(max_length=100, blank=True, null=True, verbose_name="Satisfaction with Current Method")
    
    # Desired Method
    desired_method = models.CharField(max_length=20, choices=GynecologyPatient.CONTRACEPTIVE_CHOICES, verbose_name="Desired Method")
    method_provided = models.CharField(max_length=20, choices=GynecologyPatient.CONTRACEPTIVE_CHOICES, verbose_name="Method Provided")
    
    # Counseling
    counseling_topics = models.TextField(verbose_name="Counseling Topics Discussed")
    side_effects_discussed = models.TextField(blank=True, null=True, verbose_name="Side Effects Discussed")
    
    # Follow-up
    follow_up_required = models.BooleanField(default=True, verbose_name="Follow-up Required")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    # Notes
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Contraceptive Consultation"
        verbose_name_plural = "Contraceptive Consultations"
        ordering = ['-consultation_date']
    
    def __str__(self):
        return f"Contraceptive Consultation - {self.patient.patient.full_name} ({self.consultation_date})"


class MenopauseManagement(models.Model):
    """Menopause Management"""
    patient = models.ForeignKey(GynecologyPatient, on_delete=models.CASCADE, related_name='menopause_management')
    assessment_date = models.DateField(verbose_name="Assessment Date")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='menopause_assessments', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Menopause Status
    MENOPAUSE_STATUS_CHOICES = [
        ('PREMENOPAUSAL', 'Premenopausal'),
        ('PERIMENOPAUSAL', 'Perimenopausal'),
        ('POSTMENOPAUSAL', 'Postmenopausal'),
    ]
    
    menopause_status = models.CharField(max_length=20, choices=MENOPAUSE_STATUS_CHOICES, verbose_name="Menopause Status")
    
    # Symptoms
    hot_flashes = models.BooleanField(default=False, verbose_name="Hot Flashes")
    night_sweats = models.BooleanField(default=False, verbose_name="Night Sweats")
    mood_changes = models.BooleanField(default=False, verbose_name="Mood Changes")
    sleep_disturbances = models.BooleanField(default=False, verbose_name="Sleep Disturbances")
    vaginal_dryness = models.BooleanField(default=False, verbose_name="Vaginal Dryness")
    decreased_libido = models.BooleanField(default=False, verbose_name="Decreased Libido")
    
    # Assessment
    symptom_severity = models.CharField(max_length=20, choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')], verbose_name="Symptom Severity")
    quality_of_life_impact = models.TextField(blank=True, null=True, verbose_name="Quality of Life Impact")
    
    # Treatment
    TREATMENT_TYPE_CHOICES = [
        ('NONE', 'No Treatment'),
        ('LIFESTYLE', 'Lifestyle Modifications'),
        ('HRT', 'Hormone Replacement Therapy'),
        ('NON_HORMONAL', 'Non-hormonal Medications'),
        ('ALTERNATIVE', 'Alternative Therapies'),
    ]
    
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE_CHOICES, verbose_name="Treatment Type")
    treatment_details = models.TextField(blank=True, null=True, verbose_name="Treatment Details")
    
    # Monitoring
    bone_density_assessment = models.BooleanField(default=False, verbose_name="Bone Density Assessment Done")
    cardiovascular_assessment = models.BooleanField(default=False, verbose_name="Cardiovascular Assessment Done")
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Menopause Management"
        verbose_name_plural = "Menopause Management"
        ordering = ['-assessment_date']
    
    def __str__(self):
        return f"Menopause Assessment - {self.patient.patient.full_name} ({self.assessment_date})" 