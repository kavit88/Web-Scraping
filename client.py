import requests

# =====================================================
# BASE URL
# =====================================================

BASE_URL = "http://127.0.0.1:8000"

# =====================================================
# TOKEN
# =====================================================

TOKEN = "mysecret123"

# =====================================================
# COMMON PARAMS
# =====================================================

params = {
    "api_token": TOKEN
}

# =====================================================
# GET ALL STUDENTS
# =====================================================

response = requests.get(
    f"{BASE_URL}/students",
    params={
        "api_token": TOKEN,
        "skip": 0,
        "limit": 5
    }
)

print("\n==============================")
print("GET ALL STUDENTS")
print("==============================")

print(response.json())

# =====================================================
# GET SINGLE STUDENT
# =====================================================

response = requests.get(
    f"{BASE_URL}/students/1",
    params=params
)

print("\n==============================")
print("GET SINGLE STUDENT")
print("==============================")

print(response.json())

# =====================================================
# POST API
# =====================================================

new_student = {
    "id": 999,
    "name": "NEW STUDENT",
    "roll_no": 999,
    "division": "A7",
    "marks": "25"
}

response = requests.post(
    f"{BASE_URL}/students",
    json=new_student,
    params=params
)

print("\n==============================")
print("POST API")
print("==============================")

print(response.json())

# =====================================================
# CHECK DATA AFTER POST
# =====================================================

response = requests.get(
    f"{BASE_URL}/students/999",
    params=params
)

print("\n==============================")
print("CHECK AFTER POST")
print("==============================")

print(response.json())

# =====================================================
# PUT API (FULL UPDATE)
# =====================================================

updated_student = {
    "id": 999,
    "name": "UPDATED STUDENT",
    "roll_no": 500,
    "division": "A4",
    "marks": "30"
}

response = requests.put(
    f"{BASE_URL}/students/999",
    json=updated_student,
    params=params
)

print("\n==============================")
print("PUT API")
print("==============================")

print(response.json())

# =====================================================
# CHECK DATA AFTER PUT
# =====================================================

response = requests.get(
    f"{BASE_URL}/students/999",
    params=params
)

print("\n==============================")
print("CHECK AFTER PUT")
print("==============================")

print(response.json())

# =====================================================
# PATCH API (PARTIAL UPDATE)
# =====================================================

patch_data = {
    "marks": "35"
}

response = requests.patch(
    f"{BASE_URL}/students/999",
    json=patch_data,
    params=params
)

print("\n==============================")
print("PATCH API")
print("==============================")

print(response.json())

# =====================================================
# CHECK DATA AFTER PATCH
# =====================================================

response = requests.get(
    f"{BASE_URL}/students/999",
    params=params
)

print("\n==============================")
print("CHECK AFTER PATCH")
print("==============================")

print(response.json())

response = requests.get(
    f"{BASE_URL}/students/999",
    params=params
)
print(response.json())
# =====================================================
# DELETE API
# =====================================================

response = requests.delete(
    f"{BASE_URL}/students/999",
    params=params
)

print("\n==============================")
print("DELETE API")
print("==============================")

print(response.json())

# =====================================================
# CHECK AFTER DELETE
# =====================================================

response = requests.get(
    f"{BASE_URL}/students/999",
    params=params
)

print("\n==============================")
print("CHECK AFTER DELETE")
print("==============================")

print(response.json())

# =====================================================
# HEADERS API
# =====================================================

response = requests.get(
    f"{BASE_URL}/headers",
    params=params
)

print("\n==============================")
print("HEADERS API")
print("==============================")

print(response.json())

# =====================================================
# RATE LIMIT TEST
# =====================================================

print("\n==============================")
print("RATE LIMIT TEST")
print("==============================")

for i in range(12):

    response = requests.get(
        f"{BASE_URL}/students",
        params=params
    )

    print(f"Request {i+1} --> Status Code:", response.status_code)