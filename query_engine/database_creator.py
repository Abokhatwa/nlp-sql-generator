import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()

class DatabaseCreator:
    def __init__(self):
        self.db_folder = "databases"
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
    
    def create_ecommerce_db(self):
        """Create and populate e-commerce database"""
        db_path = os.path.join(self.db_folder, "ecommerce.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS order_items")
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS customers")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20),
                created_at TIMESTAMP,
                city VARCHAR(50),
                country VARCHAR(50)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(200),
                category VARCHAR(50),
                price DECIMAL(10,2),
                stock_quantity INTEGER,
                description TEXT,
                created_at TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date TIMESTAMP,
                total_amount DECIMAL(10,2),
                status VARCHAR(20),
                shipping_address TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                subtotal DECIMAL(10,2),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        
        # Insert dummy data
        
        # Customers
        countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia']
        for i in range(100):
            cursor.execute("""
                INSERT INTO customers (first_name, last_name, email, phone, created_at, city, country)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.phone_number(),
                fake.date_time_between(start_date='-2y', end_date='now'),
                fake.city(),
                random.choice(countries)
            ))
        
        # Products
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys', 'Food']
        product_adjectives = ['Premium', 'Deluxe', 'Essential', 'Professional', 'Basic', 'Advanced']
        product_nouns = ['Laptop', 'Shirt', 'Novel', 'Tool Set', 'Basketball', 'Puzzle', 'Coffee']
        
        for i in range(50):
            category = random.choice(categories)
            cursor.execute("""
                INSERT INTO products (product_name, category, price, stock_quantity, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"{random.choice(product_adjectives)} {random.choice(product_nouns)} {i+1}",
                category,
                round(random.uniform(10, 1000), 2),
                random.randint(0, 200),
                fake.text(max_nb_chars=200),
                fake.date_time_between(start_date='-1y', end_date='now')
            ))
        
        # Orders
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        for i in range(200):
            customer_id = random.randint(1, 100)
            order_date = fake.date_time_between(start_date='-6m', end_date='now')
            cursor.execute("""
                INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
                VALUES (?, ?, ?, ?, ?)
            """, (
                customer_id,
                order_date,
                0,  # Will update after adding items
                random.choice(statuses),
                fake.address()
            ))
        
        # Order items
        for order_id in range(1, 201):
            num_items = random.randint(1, 5)
            total = 0
            for _ in range(num_items):
                product_id = random.randint(1, 50)
                quantity = random.randint(1, 5)
                
                # Get product price
                cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
                price = cursor.fetchone()[0]
                subtotal = price * quantity
                total += subtotal
                
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, product_id, quantity, price, subtotal))
            
            # Update order total
            cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (total, order_id))
        
        conn.commit()
        conn.close()
        print("✅ E-commerce database created successfully!")
    
    def create_hospital_db(self):
        """Create and populate hospital management database"""
        db_path = os.path.join(self.db_folder, "hospital.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS prescriptions")
        cursor.execute("DROP TABLE IF EXISTS appointments")
        cursor.execute("DROP TABLE IF EXISTS departments")
        cursor.execute("DROP TABLE IF EXISTS doctors")
        cursor.execute("DROP TABLE IF EXISTS patients")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                date_of_birth DATE,
                gender VARCHAR(10),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                blood_type VARCHAR(5)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                specialization VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                hire_date DATE,
                salary DECIMAL(10,2)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name VARCHAR(100),
                location VARCHAR(100),
                phone VARCHAR(20),
                head_doctor_id INTEGER,
                FOREIGN KEY (head_doctor_id) REFERENCES doctors(doctor_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                appointment_date DATETIME,
                reason TEXT,
                status VARCHAR(20),
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                medication_name VARCHAR(200),
                dosage VARCHAR(100),
                frequency VARCHAR(100),
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        """)
        
        # Insert dummy data
        
        # Patients
        blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        genders = ['Male', 'Female']
        
        for i in range(150):
            cursor.execute("""
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, blood_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fake.first_name(),
                fake.last_name(),
                fake.date_of_birth(minimum_age=1, maximum_age=90),
                random.choice(genders),
                fake.phone_number(),
                fake.email(),
                fake.address(),
                random.choice(blood_types)
            ))
        
        # Doctors
        specializations = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 
                          'Dermatology', 'Psychiatry', 'General Medicine', 'Surgery']
        
        for i in range(30):
            cursor.execute("""
                INSERT INTO doctors (first_name, last_name, specialization, phone, email, hire_date, salary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fake.first_name(),
                fake.last_name(),
                random.choice(specializations),
                fake.phone_number(),
                fake.email(),
                fake.date_between(start_date='-10y', end_date='-1m'),
                round(random.uniform(80000, 250000), 2)
            ))
        
        # Departments
        dept_names = ['Emergency', 'Cardiology', 'Neurology', 'Pediatrics', 
                     'Orthopedics', 'Radiology', 'Laboratory', 'ICU']
        
        for i, dept in enumerate(dept_names):
            cursor.execute("""
                INSERT INTO departments (department_name, location, phone, head_doctor_id)
                VALUES (?, ?, ?, ?)
            """, (
                dept,
                f"Building {random.choice(['A', 'B', 'C'])}, Floor {random.randint(1, 5)}",
                fake.phone_number(),
                random.randint(1, 30)
            ))
        
        # Appointments
        statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
        reasons = ['Regular checkup', 'Follow-up', 'Consultation', 'Emergency', 'Vaccination', 'Test results']
        
        for i in range(500):
            appointment_date = fake.date_time_between(start_date='-3m', end_date='+1m')
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                random.randint(1, 150),
                random.randint(1, 30),
                appointment_date,
                random.choice(reasons),
                'completed' if appointment_date < datetime.now() else random.choice(statuses),
                fake.text(max_nb_chars=100) if random.random() > 0.5 else None
            ))
        
        # Prescriptions
        medications = ['Amoxicillin', 'Ibuprofen', 'Metformin', 'Lisinopril', 
                      'Atorvastatin', 'Omeprazole', 'Aspirin', 'Levothyroxine']
        dosages = ['100mg', '200mg', '500mg', '10mg', '20mg', '50mg']
        frequencies = ['Once daily', 'Twice daily', 'Three times daily', 'As needed', 'Every 8 hours']
        
        for i in range(300):
            start_date = fake.date_between(start_date='-6m', end_date='today')
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, doctor_id, medication_name, dosage, frequency, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                random.randint(1, 150),
                random.randint(1, 30),
                random.choice(medications),
                random.choice(dosages),
                random.choice(frequencies),
                start_date,
                start_date + timedelta(days=random.randint(7, 90))
            ))
        
        conn.commit()
        conn.close()
        print("✅ Hospital database created successfully!")
    
    def create_school_db(self):
        """Create and populate school management database"""
        db_path = os.path.join(self.db_folder, "school.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS grades")
        cursor.execute("DROP TABLE IF EXISTS enrollments")
        cursor.execute("DROP TABLE IF EXISTS courses")
        cursor.execute("DROP TABLE IF EXISTS teachers")
        cursor.execute("DROP TABLE IF EXISTS students")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                date_of_birth DATE,
                grade_level INTEGER,
                enrollment_date DATE,
                email VARCHAR(100),
                phone VARCHAR(20)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                phone VARCHAR(20),
                hire_date DATE,
                subject_specialization VARCHAR(100)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name VARCHAR(100),
                course_code VARCHAR(20),
                credits INTEGER,
                teacher_id INTEGER,
                semester VARCHAR(20),
                year INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date DATE,
                grade VARCHAR(2),
                status VARCHAR(20),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_id INTEGER,
                assignment_name VARCHAR(100),
                grade_value DECIMAL(5,2),
                max_points DECIMAL(5,2),
                grade_date DATE,
                FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
            )
        """)
        
        # Insert dummy data
        
        # Students
        for i in range(200):
            grade_level = random.randint(9, 12)
            cursor.execute("""
                INSERT INTO students (first_name, last_name, date_of_birth, grade_level, enrollment_date, email, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fake.first_name(),
                fake.last_name(),
                fake.date_of_birth(minimum_age=14, maximum_age=19),
                grade_level,
                fake.date_between(start_date='-3y', end_date='-1m'),
                fake.email(),
                fake.phone_number()
            ))
        
        # Teachers
        subjects = ['Mathematics', 'Science', 'English', 'History', 'Computer Science', 
                   'Physical Education', 'Art', 'Music', 'Foreign Language']
        
        for i in range(25):
            cursor.execute("""
                INSERT INTO teachers (first_name, last_name, email, phone, hire_date, subject_specialization)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.phone_number(),
                fake.date_between(start_date='-15y', end_date='-1y'),
                random.choice(subjects)
            ))
        
        # Courses
        course_names = {
            'Mathematics': ['Algebra I', 'Geometry', 'Algebra II', 'Pre-Calculus', 'Calculus'],
            'Science': ['Biology', 'Chemistry', 'Physics', 'Environmental Science'],
            'English': ['English 9', 'English 10', 'American Literature', 'World Literature'],
            'History': ['World History', 'US History', 'Government', 'Economics'],
            'Computer Science': ['Intro to Programming', 'Web Development', 'Data Structures']
        }
        
        course_id = 1
        for subject, courses in course_names.items():
            for course in courses:
                cursor.execute("""
                    INSERT INTO courses (course_name, course_code, credits, teacher_id, semester, year)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    course,
                    f"{subject[:3].upper()}{random.randint(100, 499)}",
                    random.choice([3, 4, 5]),
                    random.randint(1, 25),
                    random.choice(['Fall', 'Spring']),
                    2024
                ))
        
        # Enrollments
        for student_id in range(1, 201):
            num_courses = random.randint(4, 7)
            enrolled_courses = random.sample(range(1, 20), num_courses)
            
            for course_id in enrolled_courses:
                status = random.choice(['active', 'completed', 'dropped'])
                grade = None
                if status == 'completed':
                    grade = random.choice(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'])
                
                cursor.execute("""
                    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    student_id,
                    course_id,
                    fake.date_between(start_date='-6m', end_date='today'),
                    grade,
                    status
                ))
        
        # Grades
        assignment_types = ['Homework', 'Quiz', 'Test', 'Project', 'Final Exam', 'Midterm Exam']
        
        cursor.execute("SELECT enrollment_id FROM enrollments WHERE status = 'completed' OR status = 'active'")
        enrollments = cursor.fetchall()
        
        for enrollment in enrollments:
            enrollment_id = enrollment[0]
            num_assignments = random.randint(5, 15)
            
            for i in range(num_assignments):
                max_points = random.choice([10, 20, 50, 100])
                grade_value = round(random.uniform(0.6, 1.0) * max_points, 2)
                
                cursor.execute("""
                    INSERT INTO grades (enrollment_id, assignment_name, grade_value, max_points, grade_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    enrollment_id,
                    f"{random.choice(assignment_types)} {i+1}",
                    grade_value,
                    max_points,
                    fake.date_between(start_date='-6m', end_date='today')
                ))
        
        conn.commit()
        conn.close()
        print("✅ School database created successfully!")
    
    def create_all_databases(self):
        """Create all databases"""
        print("Creating all databases...")
        self.create_ecommerce_db()
        self.create_hospital_db()
        self.create_school_db()
        print("✅ All databases created successfully!")


if __name__ == "__main__":
    creator = DatabaseCreator()
    creator.create_all_databases()