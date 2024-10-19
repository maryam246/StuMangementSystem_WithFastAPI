from fastapi import FastAPI, APIRouter, HTTPException
from configuration import collection
from Database.schemas import all_students, individual_data
from Database.models import Student
from bson.objectid import ObjectId
from datetime import datetime, timezone

app = FastAPI()
router = APIRouter()

# Mapping of programs to their corresponding departments
program_department_mapping = {
    "BS Computer Science": "Computer Science Department",
    "BS Business Administration": "Business Administration Department",
    "BS Mathematics": "Mathematics Department",
    "BS Psychology": "Psychology Department",
    "BS English": "English Department",
}

def generate_student_id() -> str:
    last_student = collection.find_one(sort=[("student_id", -1)])  # Fetch the last student record
    if last_student and 'student_id' in last_student:
        last_stu_id = last_student['student_id']
        new_stu_number = int(last_stu_id[2:]) + 1
        return f"bc{new_stu_number:05}"  # Generate the new student ID
    return "bc00001"  # Default first student ID

# Endpoint to get all students
@router.get("/get-all")
async def get_all_students():
    data = collection.find()  # Fetch all student records from the database
    return all_students(data)

# Endpoint to get student by MongoDB Object ID
@router.get("/get-by-id")
async def get_student_by_mongo_id(mongo_id: str):
    try:
        student = collection.find_one({"_id": ObjectId(mongo_id)})  # Find student by MongoDB's Object ID
        if not student:
            raise HTTPException(status_code=404, detail="Student not found by Object ID")
        return individual_data(student)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Object ID format: {e}")

# Endpoint to get student by custom student ID
@router.get("/get-stu-id")
async def get_student_by_student_id(stu_id: str):
    student = collection.find_one({"student_id": stu_id})  # Find student by custom student ID
    if not student:
        raise HTTPException(status_code=404, detail="Student not found by custom student ID")
    return individual_data(student)

# Endpoint to create a new student
@router.post("/create")
async def create_student(new_student: Student):
    # Validate program and department relationship
    expected_department = program_department_mapping.get(new_student.program)
    if expected_department != new_student.department:
        raise HTTPException(status_code=400, detail="Selected program and department do not match. Please enter related program and department.")

    # Generate student ID (server-side only)
    student_id = generate_student_id()

    # Insert the new student record
    new_student_dict = new_student.dict()
    new_student_dict["student_id"] = student_id  # Add generated student_id to the data

    resp = collection.insert_one(new_student_dict)
    return {"status_code": 200, "id": str(resp.inserted_id), "student_id": student_id}

# Endpoint to update a student by custom student ID
@router.put("/update-stu-id")
async def update_student(stu_id: str, updated_student: Student):
    student = collection.find_one({"student_id": stu_id})  # Find student by custom student ID
    if not student:
        raise HTTPException(status_code=404, detail="Student not found by custom student ID")
    
    updated_student.updated_at = datetime.now(timezone.utc)  # Update the timestamp
    collection.update_one({"student_id": stu_id}, {"$set": updated_student.dict(exclude={"student_id"})})
    return {"status_code": 200, "message": "Student updated successfully."}

# Endpoint to delete a student by custom student ID
@router.delete("/delete-stu-id")
async def delete_student_by_student_id(stu_id: str):
    result = collection.delete_one({"student_id": stu_id})  # Delete student by custom student ID
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found by custom student ID")
    return {"status_code": 200, "message": "Student deleted successfully."}

app.include_router(router)
