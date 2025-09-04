from django.contrib import admin 
from .models import Patient, Doctor, PatientDoctorMap 

@admin.register(Patient) 
class PatientAdmin(admin.ModelAdmin): 
    list_display = ("id", "first_name", "last_name", "age", "gender", "created_by", "created_at") 
    search_fields = ("first_name", "last_name", "created_by__email") 
    list_filter = ("gender",) 
    
@admin.register(Doctor) 
class DoctorAdmin(admin.ModelAdmin): 
    list_display = ("id", "name", "specialization", "email", "phone") 
    search_fields = ("name", "email", "specialization") 
    
@admin.register(PatientDoctorMap) 
class PatientDoctorMapAdmin(admin.ModelAdmin): 
    list_display = ("id", "patient", "doctor", "assigned_by", "created_at") 
    search_fields = ("patient__first_name", "doctor__name")