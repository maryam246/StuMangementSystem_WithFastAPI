from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime

# Pydantic model for validating student data
class Student(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter Student Name")  
    father_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter Father Name")
    age: int = Field(..., ge=15, le=30, example=20) 
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$", example="Enter 11 digit phone number")
    email: EmailStr = Field(..., example="Enter email like student@example.com")
    address: str = Field(..., min_length=1, max_length=100, example="Enter Address")

    # Predefined Campus, Program, Department options
    campus: Literal["VU Lahore Campus", "VU Karachi Campus", 
                    "VU Islamabad Campus", "VU Faisalabad Campus", 
                    "VU Multan Campus"] = Field(example="Enter Campus")
    
    program: Literal["BS Computer Science", "BS Business Administration", 
                     "BS Mathematics", "BS Psychology", "BS English"] = Field(example="Enter Program")
    
    department: Literal["Computer Science Department", "Business Administration Department", 
                        "Mathematics Department", "Psychology Department",
                        "English Department"] = Field(example="Enter Department")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Default to UTC time at creation
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Default to UTC time at update

    class Config:
        from_attributes = True
