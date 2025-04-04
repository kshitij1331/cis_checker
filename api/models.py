from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class ComplianceReport(models.Model):
    system_name = models.CharField(max_length=255)
    scan_Date = models.DateTimeField(auto_now_add=True)
    compliance_score = models.FloatField()
    report_data = models.JSONField()
    status = models.CharField(max_length=50, choices=[('Pass', 'Pass'), ('FAIL', 'Fail')])


    def __str__(self):
        return f"{self.system_name} - {self.scan_Date.strftime('%Y-%m-%d')} - {self.compliance_score}"
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('auditor', 'Auditor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

class Server(models.Model):
    """Stores information about remote servers"""
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=50)
    ssh_key_path = models.CharField(max_length=255)  # Path to private SSH key

    def __str__(self):
        return self.name