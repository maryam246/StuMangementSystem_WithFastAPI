from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime

# Pydantic model for validating student data
class Student(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$")  # Only letters and spaces allowed
    father_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$")  # Only letters and spaces allowed
    age: int = Field(..., ge=15, le=30)  # Age must be between 15 and 30
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")  # Exactly 11 digits
    email: EmailStr  # Must be a valid email format
    address: str = Field(..., min_length=1, max_length=100)  # Address limited to 100 characters

    # Predefined Campus, Program, Department options
    campus: Literal["VU Lahore Campus", "VU Karachi Campus", 
                    "VU Islamabad Campus", "VU Faisalabad Campus", 
                    "VU Multan Campus"]
    
    program: Literal["BS Computer Science", "BS Business Administration", 
                     "BS Mathematics", "BS Psychology", "BS English"]
    
    department: Literal["Computer Science Department", "Business Administration Department", 
                        "Mathematics Department", "Psychology Department",
                        "English Department"]
    
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Default to UTC time at creation
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Default to UTC time at update

    class Config:
        orm_mode = True
