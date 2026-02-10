
import sqlite3

# Test Script: College Management System
# 1. Creates Tables
# 2. Inserts Helper Data
# 3. Queries Results

try:
    print("Step 1: Creating Database...")
    conn = sqlite3.connect(":memory:") # Using RAM for fast testing
    cursor = conn.cursor()

    # Create Tables
    print("Step 2: Creating Tables (Students, Courses)...")
    cursor.executescript("""
        CREATE TABLE Students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            major TEXT
        );
        
        CREATE TABLE Courses (
            course_id INTEGER PRIMARY KEY,
            title TEXT,
            credits INTEGER
        );
        
        INSERT INTO Students (name, major) VALUES 
        ('Rahul', 'Engineering'), 
        ('Priya', 'Medicine'), 
        ('Amit', 'Commerce');
        
        INSERT INTO Courses (title, credits) VALUES 
        ('Advanced AI', 4), 
        ('Anatomy 101', 3), 
        ('Accounting', 3);
    """)
    conn.commit()

    # Query Data
    print("Step 3: Querying Data to Verify...")
    print("-" * 40)
    
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    print("STUDENTS TABLE:")
    for s in students:
        print(s)
        
    print("-" * 40)
    
    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()
    print("COURSES TABLE:")
    for c in courses:
        print(c)
        
    print("-" * 40)
    print("✅ TEST PASSED: SQL Code ran successfully!")
    
except Exception as e:
    print(f"❌ TEST FAILED: {e}")

finally:
    if conn: conn.close()
