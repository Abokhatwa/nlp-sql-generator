DATABASES = {
    "E-Commerce": {
        "description": "An e-commerce database for online shopping",
        "tables": {
            "customers": {
                "columns": [
                    "customer_id (INT, PRIMARY KEY)",
                    "first_name (VARCHAR(50))",
                    "last_name (VARCHAR(50))",
                    "email (VARCHAR(100), UNIQUE)",
                    "phone (VARCHAR(20))",
                    "created_at (TIMESTAMP)",
                    "city (VARCHAR(50))",
                    "country (VARCHAR(50))"
                ],
                "description": "Stores customer information"
            },
            "products": {
                "columns": [
                    "product_id (INT, PRIMARY KEY)",
                    "product_name (VARCHAR(200))",
                    "category (VARCHAR(50))",
                    "price (DECIMAL(10,2))",
                    "stock_quantity (INT)",
                    "description (TEXT)",
                    "created_at (TIMESTAMP)"
                ],
                "description": "Stores product information"
            },
            "orders": {
                "columns": [
                    "order_id (INT, PRIMARY KEY)",
                    "customer_id (INT, FOREIGN KEY references customers)",
                    "order_date (TIMESTAMP)",
                    "total_amount (DECIMAL(10,2))",
                    "status (VARCHAR(20))",
                    "shipping_address (TEXT)"
                ],
                "description": "Stores order information"
            },
            "order_items": {
                "columns": [
                    "order_item_id (INT, PRIMARY KEY)",
                    "order_id (INT, FOREIGN KEY references orders)",
                    "product_id (INT, FOREIGN KEY references products)",
                    "quantity (INT)",
                    "unit_price (DECIMAL(10,2))",
                    "subtotal (DECIMAL(10,2))"
                ],
                "description": "Stores individual items in each order"
            }
        }
    },
    
    "Hospital Management": {
        "description": "A hospital management database",
        "tables": {
            "patients": {
                "columns": [
                    "patient_id (INT, PRIMARY KEY)",
                    "first_name (VARCHAR(50))",
                    "last_name (VARCHAR(50))",
                    "date_of_birth (DATE)",
                    "gender (VARCHAR(10))",
                    "phone (VARCHAR(20))",
                    "email (VARCHAR(100))",
                    "address (TEXT)",
                    "blood_type (VARCHAR(5))"
                ],
                "description": "Stores patient information"
            },
            "doctors": {
                "columns": [
                    "doctor_id (INT, PRIMARY KEY)",
                    "first_name (VARCHAR(50))",
                    "last_name (VARCHAR(50))",
                    "specialization (VARCHAR(100))",
                    "phone (VARCHAR(20))",
                    "email (VARCHAR(100))",
                    "hire_date (DATE)",
                    "salary (DECIMAL(10,2))"
                ],
                "description": "Stores doctor information"
            },
            "appointments": {
                "columns": [
                    "appointment_id (INT, PRIMARY KEY)",
                    "patient_id (INT, FOREIGN KEY references patients)",
                    "doctor_id (INT, FOREIGN KEY references doctors)",
                    "appointment_date (DATETIME)",
                    "reason (TEXT)",
                    "status (VARCHAR(20))",
                    "notes (TEXT)"
                ],
                "description": "Stores appointment information"
            },
            "prescriptions": {
                "columns": [
                    "prescription_id (INT, PRIMARY KEY)",
                    "patient_id (INT, FOREIGN KEY references patients)",
                    "doctor_id (INT, FOREIGN KEY references doctors)",
                    "medication_name (VARCHAR(200))",
                    "dosage (VARCHAR(100))",
                    "frequency (VARCHAR(100))",
                    "start_date (DATE)",
                    "end_date (DATE)"
                ],
                "description": "Stores prescription information"
            },
            "departments": {
                "columns": [
                    "department_id (INT, PRIMARY KEY)",
                    "department_name (VARCHAR(100))",
                    "location (VARCHAR(100))",
                    "phone (VARCHAR(20))",
                    "head_doctor_id (INT, FOREIGN KEY references doctors)"
                ],
                "description": "Stores hospital department information"
            }
        }
    },
    
    "School Management": {
        "description": "A school management database",
        "tables": {
            "students": {
                "columns": [
                    "student_id (INT, PRIMARY KEY)",
                    "first_name (VARCHAR(50))",
                    "last_name (VARCHAR(50))",
                    "date_of_birth (DATE)",
                    "grade_level (INT)",
                    "enrollment_date (DATE)",
                    "email (VARCHAR(100))",
                    "phone (VARCHAR(20))"
                ],
                "description": "Stores student information"
            },
            "teachers": {
                "columns": [
                    "teacher_id (INT, PRIMARY KEY)",
                    "first_name (VARCHAR(50))",
                    "last_name (VARCHAR(50))",
                    "email (VARCHAR(100))",
                    "phone (VARCHAR(20))",
                    "hire_date (DATE)",
                    "subject_specialization (VARCHAR(100))"
                ],
                "description": "Stores teacher information"
            },
            "courses": {
                "columns": [
                    "course_id (INT, PRIMARY KEY)",
                    "course_name (VARCHAR(100))",
                    "course_code (VARCHAR(20))",
                    "credits (INT)",
                    "teacher_id (INT, FOREIGN KEY references teachers)",
                    "semester (VARCHAR(20))",
                    "year (INT)"
                ],
                "description": "Stores course information"
            },
            "enrollments": {
                "columns": [
                    "enrollment_id (INT, PRIMARY KEY)",
                    "student_id (INT, FOREIGN KEY references students)",
                    "course_id (INT, FOREIGN KEY references courses)",
                    "enrollment_date (DATE)",
                    "grade (VARCHAR(2))",
                    "status (VARCHAR(20))"
                ],
                "description": "Stores student course enrollments"
            },
            "grades": {
                "columns": [
                    "grade_id (INT, PRIMARY KEY)",
                    "enrollment_id (INT, FOREIGN KEY references enrollments)",
                    "assignment_name (VARCHAR(100))",
                    "grade_value (DECIMAL(5,2))",
                    "max_points (DECIMAL(5,2))",
                    "grade_date (DATE)"
                ],
                "description": "Stores student grades"
            }
        }
    }
}


def get_schema_prompt(database_name):
    """Generate a formatted schema description for the selected database"""
    if database_name not in DATABASES:
        return ""
    
    db = DATABASES[database_name]
    schema_text = f"Database: {database_name}\n"
    schema_text += f"Description: {db['description']}\n\n"
    schema_text += "Tables:\n"
    
    for table_name, table_info in db['tables'].items():
        schema_text += f"\nTable: {table_name}\n"
        schema_text += f"Description: {table_info['description']}\n"
        schema_text += "Columns:\n"
        for column in table_info['columns']:
            schema_text += f"  - {column}\n"
    
    return schema_text