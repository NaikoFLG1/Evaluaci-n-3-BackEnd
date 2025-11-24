import requests

BASE_URL = 'http://127.0.0.1:8000'

# 1. Login
print("=== LOGIN ===")
login_response = requests.post(
    f'{BASE_URL}/api/auth/login/',
    json={'username': 'admin', 'password': 'administrador123.'}
)
print(f"Status: {login_response.status_code}")
print(f"Response: {login_response.json()}\n")

if login_response.status_code == 200:
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Listar vehículos
    print("=== LISTAR VEHÍCULOS ===")
    vehicles_response = requests.get(f'{BASE_URL}/api/vehicles/', headers=headers)
    print(f"Status: {vehicles_response.status_code}")
    print(f"Response: {vehicles_response.json()}\n")
    
    # 3. Crear vehículo
    print("=== CREAR VEHÍCULO ===")
    new_vehicle = {
        'plate': 'ABCD12',
        'type': 'truck',
        'owner': 'Transportes del Sur',
        'status': 'active',
        'tech_review_due': '2026-12-31',
        'capacity_kg': 15000
    }
    create_response = requests.post(
        f'{BASE_URL}/api/vehicles/',
        json=new_vehicle,
        headers=headers
    )
    print(f"Status: {create_response.status_code}")
    print(f"Response: {create_response.json()}\n")
    
    # 4. Listar registros de acceso
    print("=== LISTAR REGISTROS DE ACCESO ===")
    records_response = requests.get(f'{BASE_URL}/api/access-records/', headers=headers)
    print(f"Status: {records_response.status_code}")
    print(f"Response: {records_response.json()}\n")

else:
    print("❌ Login falló. Verifica username y password.")
