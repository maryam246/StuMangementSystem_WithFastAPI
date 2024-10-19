from bson import ObjectId
from datetime import datetime

# Function to format individual student data into a dictionary
def individual_data(student):
    return {
        "id": str(student["_id"]),  # MongoDB Object ID
        "student_id": student["student_id"],  # Custom student ID
        "full_name": student["full_name"],
        "father_name": student["father_name"],
        "age": student["age"],
        "phone": student["phone"],
        "email": student["email"],
        "address": student["address"],
        "campus": student["campus"],
        "program": student["program"],
        "department": student["department"],
        "created_at": student["created_at"].strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": student["updated_at"].strftime('%Y-%m-%d %H:%M:%S'),
    }

# Function to apply the 'individual_data' transformation to a list of students
def all_students(students):
    return [individual_data(student) for student in students]  # Return the list of formatted student data
