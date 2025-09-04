from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

from .views import RegisterView, PatientViewSet, DoctorViewSet, PatientDoctorMapViewSet 

router = DefaultRouter() 
router.register(r"patients", PatientViewSet, basename="patient") 
router.register(r"doctors", DoctorViewSet, basename="doctor") 
router.register(r"mappings", PatientDoctorMapViewSet, basename="mapping") 

urlpatterns = [ 
    path("auth/register/", RegisterView.as_view(), name="register"), 
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"), 
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  
    path("", include(router.urls)), 
]