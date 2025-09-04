from django.contrib.auth.models import User 
from django.db import IntegrityError 
from rest_framework import serializers 
from .models import Patient, Doctor, PatientDoctorMap 
from .validators import validate_age

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150) 
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def create(self, validated_data):
        name = validated_data.get("name").strip() 
        email = validated_data.get("email").lower() 
        password = validated_data.get("password")

        user = User.objects.create_user(username=email, email=email, first_name=name)
        user.set_password(password) 
        user.save() 
        return user

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ["id", "first_name", "email"]

class PatientSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True) 
    first_name = serializers.CharField(max_length=100) 
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True) 
    age = serializers.IntegerField(validators=[validate_age])

    class Meta: 
        model = Patient 
        fields = [ "id", "first_name", "last_name", "age", "gender", "address", "created_by", "created_at", "updated_at", ] 
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

class DoctorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Doctor 
        fields = ["id", "name", "specialization", "email", "phone", "created_at", "updated_at"] 
        read_only_fields = ["id", "created_at", "updated_at"]

class PatientDoctorMapSerializer(serializers.ModelSerializer): 
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all()) 
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta: 
        model = PatientDoctorMap
        fields = ["id", "patient", "doctor", "assigned_by", "created_at", "updated_at"] 
        read_only_fields = ["id", "assigned_by", "created_at", "updated_at"]

        def validate(self, attrs): 
            patient = attrs.get("patient") 
            request = self.context.get("request") 
            if request and request.user.is_authenticated:  
                if patient.created_by_id != request.user.id: 
                    raise serializers.ValidationError("You can only map doctors for patients you created.") 
            return attrs
        
        def create(self, validated_data): 
            try: 
                validated_data["assigned_by"] = self.context["request"].user 
                return super().create(validated_data) 
            except IntegrityError: 
                raise serializers.ValidationError("This doctor is already assigned to the patient.")