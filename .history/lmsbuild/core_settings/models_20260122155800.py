class AdminSettings(models.Model):
    # GENERAL
    site_name = models.CharField(max_length=200, default="My LMS")
    maintenance_mode = models.BooleanField(default=False)

    # ATTENDANCE
    attendance_enabled = models.BooleanField(default=True)
    gps_required = models.BooleanField(default=True)
    gps_radius = models.IntegerField(default=100)
    half_day_hours = models.FloatField(default=4.0)
    attendance_approval_required = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)

    @staticmethod
    def get():
        return AdminSettings.objects.get_or_create(pk=1)[0]
