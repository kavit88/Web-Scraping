from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import json
import uvicorn

# =====================================================
# CREATE FASTAPI SERVER
# =====================================================

app = FastAPI(title="Student Management API")

# =====================================================
# RATE LIMITING
# =====================================================

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

# =====================================================
# SECRET TOKEN
# =====================================================

API_TOKEN = "mysecret123"

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def load_students():

    with open("students.json", "r", encoding="utf-8") as file:

        return json.load(file)


def save_students(data):

    with open("students.json", "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)


def verify_token(token):

    if token != API_TOKEN:

        raise HTTPException(
            status_code=401,
            detail="Invalid API Token"
        )

# =====================================================
# PYDANTIC MODELS
# =====================================================

class Student(BaseModel):

    id: int
    name: str
    roll_no: int
    division: str
    marks: str


class UpdateStudent(BaseModel):

    name: Optional[str] = None
    roll_no: Optional[int] = None
    division: Optional[str] = None
    marks: Optional[str] = None

# =====================================================
# HOME API
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Student API Server Running"
    }

# =====================================================
# GET ALL STUDENTS
# =====================================================

@app.get("/students")
@limiter.limit("10/minute")
def get_students(
    request: Request,
    skip: int = 0,
    limit: int = 5,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    return students[skip : skip + limit]

# =====================================================
# GET SINGLE STUDENT
# =====================================================

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    for student in students:

        if student["id"] == student_id:

            return student

    return {
        "error": "Student not found"
    }

# =====================================================
# POST API
# =====================================================

@app.post("/students")
def add_student(
    student: Student,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    # CHECK DUPLICATE ID

    for s in students:

        if s["id"] == student.id:

            return {
                "error": "Student ID already exists"
            }

    # ADD STUDENT

    students.append(student.dict())

    # SAVE UPDATED DATA

    save_students(students)

    return {
        "message": "Student added successfully",
        "data": student
    }

# =====================================================
# PUT API (FULL UPDATE)
# =====================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    for i, student in enumerate(students):

        if student["id"] == student_id:

            students[i] = updated_student.dict()

            save_students(students)

            return {
                "message": "Student updated successfully",
                "data": updated_student
            }

    return {
        "error": "Student not found"
    }

# =====================================================
# PATCH API (PARTIAL UPDATE)
# =====================================================

@app.patch("/students/{student_id}")
def patch_student(
    student_id: int,
    updated_data: UpdateStudent,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    for student in students:

        if student["id"] == student_id:

            if updated_data.name is not None:

                student["name"] = updated_data.name

            if updated_data.roll_no is not None:

                student["roll_no"] = updated_data.roll_no

            if updated_data.division is not None:

                student["division"] = updated_data.division

            if updated_data.marks is not None:

                student["marks"] = updated_data.marks

            save_students(students)

            return {
                "message": "Student patched successfully",
                "data": student
            }

    return {
        "error": "Student not found"
    }

# =====================================================
# DELETE API
# =====================================================

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    api_token: str = None
):

    verify_token(api_token)

    students = load_students()

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            save_students(students)

            return {
                "message": "Student deleted successfully"
            }

    return {
        "error": "Student not found"
    }

# =====================================================
# HEADERS API
# =====================================================

@app.get("/headers")
def get_headers(
    request: Request,
    api_token: str = None
):

    verify_token(api_token)

    return {
        "headers": dict(request.headers)
    }

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )