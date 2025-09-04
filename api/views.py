from django.contrib.auth.models import User 
from rest_framework import viewsets, status, generics, mixins 
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound

from .models import Patient, Doctor, PatientDoctorMap 
from .serializers import ( 
    RegisterSerializer, 
    UserSerializer, 
    PatientSerializer, 
    DoctorSerializer, 
    PatientDoctorMapSerializer, ) 

from .permissions import IsOwnerOrReadOnly

class RegisterView(generics.CreateAPIView): 
    permission_classes = [AllowAny] 
    serializer_class = RegisterSerializer 

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        user = serializer.save() 
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
class PatientViewSet(viewsets.ModelViewSet): 
    serializer_class = PatientSerializer 
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly] 

    def get_queryset(self): 
         return Patient.objects.filter(created_by=self.request.user).order_by("created_at") 
    
    def perform_create(self, serializer): 
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet): 
    queryset = Doctor.objects.all() 
    serializer_class = DoctorSerializer 
    permission_classes = [IsAuthenticated]

class PatientDoctorMapViewSet(viewsets.ModelViewSet): 
    queryset = PatientDoctorMap.objects.select_related("patient", "doctor").all() 
    serializer_class = PatientDoctorMapSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        qs = super().get_queryset() 
        return qs.filter(patient__created_by=self.request.user) 
    
    @action(detail=False, methods=["get"], url_path=r"(?P<patient_id>[^/.]+)") 
    
    def list_for_patient(self, request, patient_id=None): 
        try: 
            patient = Patient.objects.get(pk=patient_id, created_by=request.user) 
        except Patient.DoesNotExist: 
            raise NotFound("Patient not found or not owned by you.")
         
        mappings = self.get_queryset().filter(patient=patient) 
        serializer = self.get_serializer(mappings, many=True) 
        return Response(serializer.data)