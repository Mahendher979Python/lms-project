from django.db import models


class AdminSettings(models.Model):

    # =========================
    # GENERAL SETTINGS
    # =========================
    site_name = models.CharField(max_length=200, default="My LMS")
    site_logo = models.ImageField(upload_to="settings/", null=True, blank=True)
    support_email = models.EmailField(blank=True, null=True)
    support_mobile = models.CharField(max_length=20, blank=True, null=True)
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    default_language = models.CharField(max_length=20, default="en")
    maintenance_mode = models.BooleanField(default=False)

    # =========================
    # USER & AUTH SETTINGS
    # =========================
    allow_self_registration = models.BooleanField(default=True)
    default_user_role = models.CharField(
        max_length=20,
        choices=(("student", "Student"), ("trainer", "Trainer")),
        default="student"
    )
    email_verification_required = models.BooleanField(default=False)
    mobile_otp_required = models.BooleanField(default=False)
    max_login_attempts = models.IntegerField(default=5)
    session_timeout_minutes = models.IntegerField(default=60)

    # =========================
    # STUDENT SETTINGS
    # =========================
    student_approval_required = models.BooleanField(default=False)
    max_courses_per_student = models.IntegerField(default=5)
    student_attendance_required_percent = models.IntegerField(default=75)
    auto_block_student_inactive_days = models.IntegerField(default=90)

    # =========================
    # TRAINER SETTINGS
    # =========================
    trainer_approval_required = models.BooleanField(default=True)
    trainer_can_create_courses = models.BooleanField(default=True)
    max_courses_per_trainer = models.IntegerField(default=5)
    trainer_attendance_required = models.BooleanField(default=True)
    trainer_daily_work_hours = models.FloatField(default=8.0)
    trainer_late_login_minutes = models.IntegerField(default=15)

    # =========================
    # COURSE SETTINGS
    # =========================
    course_approval_required = models.BooleanField(default=True)
    course_visibility_default = models.CharField(
        max_length=20,
        choices=(("public", "Public"), ("private", "Private")),
        default="private"
    )
    course_validity_days = models.IntegerField(default=180)
    max_students_per_course = models.IntegerField(default=100)
    allow_course_preview = models.BooleanField(default=True)

    # =========================
    # ATTENDANCE SETTINGS
    # =========================
    attendance_enabled = models.BooleanField(default=True)
    gps_required = models.BooleanField(default=True)
    gps_radius_meters = models.IntegerField(default=100)
    attendance_login_start = models.TimeField(null=True, blank=True)
    attendance_login_end = models.TimeField(null=True, blank=True)
    auto_logout_enabled = models.BooleanField(default=True)
    auto_logout_time = models.TimeField(null=True, blank=True)
    half_day_hours = models.FloatField(default=4.0)
    late_mark_minutes = models.IntegerField(default=10)
    attendance_approval_required = models.BooleanField(default=True)
    allow_manual_attendance = models.BooleanField(default=False)

    # =========================
    # LEAVE & HOLIDAY
    # =========================
    leave_module_enabled = models.BooleanField(default=False)
    max_leaves_per_month = models.IntegerField(default=2)
    leave_approval_required = models.BooleanField(default=True)

    # =========================
    # ASSIGNMENT & EXAM
    # =========================
    assignment_enabled = models.BooleanField(default=True)
    late_submission_allowed = models.BooleanField(default=True)
    late_submission_penalty_percent = models.IntegerField(default=10)
    exam_enabled = models.BooleanField(default=True)
    passing_percentage = models.IntegerField(default=40)

    # =========================
    # CERTIFICATE SETTINGS
    # =========================
    certificate_enabled = models.BooleanField(default=True)
    certificate_attendance_percent = models.IntegerField(default=75)
    certificate_auto_generate = models.BooleanField(default=True)
    certificate_qr_enabled = models.BooleanField(default=True)

    # =========================
    # CONTENT & FILE SETTINGS
    # =========================
    max_file_upload_mb = models.IntegerField(default=50)
    allowed_file_types = models.TextField(
        default="pdf,docx,pptx,mp4,zip"
    )
    video_streaming_enabled = models.BooleanField(default=True)
    allow_download_materials = models.BooleanField(default=True)

    # =========================
    # NOTIFICATION SETTINGS
    # =========================
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    whatsapp_notifications = models.BooleanField(default=False)
    attendance_alerts = models.BooleanField(default=True)
    exam_alerts = models.BooleanField(default=True)

    # =========================
    # REPORTS SETTINGS
    # =========================
    reports_enabled = models.BooleanField(default=True)
    allow_excel_export = models.BooleanField(default=True)
    allow_pdf_export = models.BooleanField(default=False)
    report_retention_days = models.IntegerField(default=365)

    # =========================
    # SECURITY SETTINGS
    # =========================
    two_factor_auth = models.BooleanField(default=False)
    ip_restriction_enabled = models.BooleanField(default=False)
    audit_logs_enabled = models.BooleanField(default=True)
    data_backup_enabled = models.BooleanField(default=True)
    backup_frequency_days = models.IntegerField(default=7)

    updated_at = models.DateTimeField(auto_now=True)

    # =========================
    # SINGLETON ENFORCE
    # =========================
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @staticmethod
    def get():
        return AdminSettings.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return "Admin Global Settings"


class TrainerSettings(models.Model):

    # ======================
    # GENERAL
    # ======================
    approval_required = models.BooleanField(default=True)
    profile_editable = models.BooleanField(default=True)

    # ======================
    # COURSES
    # ======================
    can_create_courses = models.BooleanField(default=True)
    course_approval_required = models.BooleanField(default=True)
    max_courses = models.IntegerField(default=5)

    # ======================
    # ATTENDANCE
    # ======================
    attendance_mandatory = models.BooleanField(default=True)
    daily_work_hours = models.FloatField(default=8.0)
    late_login_minutes = models.IntegerField(default=15)
    attendance_approval_required = models.BooleanField(default=True)

    # ======================
    # PAYMENT
    # ======================
    payment_enabled = models.BooleanField(default=False)
    payment_type = models.CharField(
        max_length=20,
        choices=(("hourly","Hourly"),("monthly","Monthly")),
        default="hourly"
    )
    hourly_rate = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    # ======================
    # SINGLETON
    # ======================
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @staticmethod
    def get():
        return TrainerSettings.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return "Trainer Global Settings"
