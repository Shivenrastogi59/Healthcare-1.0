# Django Healthcare Backend (DRF + PostgreSQL + JWT)

A production-ready backend for a healthcare application built using **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, and **JWT authentication** via `djangorestframework-simplejwt`.

## Features
- User registration & JWT-based login  
- CRUD for Patients & Doctors  
- Patient–Doctor mapping with uniqueness constraint  
- Per-user data ownership for patients  
- Validation & robust error handling  
- Environment-based configuration  
- Dockerized with `Dockerfile` and `docker-compose.yml`

---

## API Overview

### Auth
- `POST /api/auth/register/` → Register a new user  
- `POST /api/auth/login/` → Login and get JWT tokens  
- `POST /api/auth/refresh/` → Refresh access token  

### Patients
- `POST /api/patients/` → Create patient (auth required)  
- `GET /api/patients/` → List all patients created by the user  
- `GET /api/patients/<id>/` → Retrieve patient (must own)  
- `PUT /api/patients/<id>/` → Update patient (must own)  
- `DELETE /api/patients/<id>/` → Delete patient (must own)  

### Doctors
- `POST /api/doctors/` → Add doctor (auth required)  
- `GET /api/doctors/` → List all doctors  
- `GET/PUT/DELETE /api/doctors/<id>/` → Manage doctor  

### Mappings (Doctor ↔ Patient)
- `POST /api/mappings/` → Assign doctor to patient  
- `GET /api/mappings/` → List mappings for your patients  
- `GET /api/mappings/<patient_id>/` → List doctors for a patient  
- `DELETE /api/mappings/<id>/` → Remove mapping  

---

## Testing with cURL

### 1. Register
```sh
curl -X POST http://127.0.0.1:8000/api/auth/register/ 
-H "Content-Type: application/json" 
-d '{"name": "Alice", "email": "alice@example.com", "password": "P@ssw0rd123"}'
```
### 2. Login
```sh
curl -X POST http://127.0.0.1:8000/api/auth/login/ 
-H "Content-Type: application/json" 
-d '{"username": "alice@example.com", "password": "P@ssw0rd123"}'
# Response: {"access": "...", "refresh": "..."}
```
### 3. Create Patient
```sh
ACCESS=PASTE_ACCESS_TOKEN
curl -X POST http://127.0.0.1:8000/api/patients/ 
-H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" 
-d '{"first_name":"John","last_name":"Doe","age":34,"gender":"male","address":"221B Baker St"}'
```
### 4. List My Patients
```sh
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/patients/
```
### 5. CRUD Patient by ID
```sh
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/patients/1/

curl -X PUT -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" 
-d '{"first_name":"Johnny","last_name":"Doe","age":35,"gender":"male","address":"New Address"}' 
http://127.0.0.1:8000/api/patients/1/

curl -X DELETE -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/patients/1/
```
### 6. Add Doctor
```sh
curl -X POST http://127.0.0.1:8000/api/doctors/ 
-H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" 
-d '{"name":"Dr. House","specialization":"Diagnostics","email":"house@ppth.org","phone":"+1-555-000"}'
```
### 7. List Doctors
```sh
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/doctors/
```
### 8. Map Doctor to Patient
```sh
curl -X POST http://127.0.0.1:8000/api/mappings/ 
-H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" 
-d '{"patient": 1, "doctor": 1}'
```
### 9. List All Mappings
```sh
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/mappings/
```
### 10. List Doctors Assigned to a Patient
```sh
curl -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/mappings/1/
```
### 11. Remove Mapping
```sh
curl -X DELETE -H "Authorization: Bearer $ACCESS" http://127.0.0.1:8000/api/mappings/3/
```

---

## Running with Docker
```sh
docker-compose up --build
```