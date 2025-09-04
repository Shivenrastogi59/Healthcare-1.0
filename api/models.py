from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Patient(TimeStampedModel):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Doctor(TimeStampedModel):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class PatientDoctorMap(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="mappings")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("patient", "doctor")
        verbose_name = "Patient–Doctor Mapping"
        verbose_name_plural = "Patient–Doctor Mappings"

    def __str__(self):
        return f"{self.patient} → {self.doctor}"