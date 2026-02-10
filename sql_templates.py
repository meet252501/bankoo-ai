"""
SQL Template Generator for Bankoo AI
Automatically generates SQL code from Gujarati/English prompts
"""

SQL_TEMPLATES = {
    "college_management": """-- College Management System
CREATE TABLE Students (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  roll_no INT,
  email VARCHAR(255),
  branch VARCHAR(255),
  semester INT
);

CREATE TABLE Teachers (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  subject VARCHAR(255)
);

CREATE TABLE Subjects (
  id INT PRIMARY KEY,
  subject_name VARCHAR(255),
  teacher_id INT,
  FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
);

CREATE TABLE Attendance (
  id INT PRIMARY KEY,
  student_id INT,
  subject_id INT,
  attendance_date DATE,
  attendance_status VARCHAR(10),
  FOREIGN KEY (student_id) REFERENCES Students(id),
  FOREIGN KEY (subject_id) REFERENCES Subjects(id)
);

-- Sample Data
INSERT INTO Students VALUES (1, 'Arvind Patel', 101, 'arvind@example.com', 'Computer Science', 1);
INSERT INTO Students VALUES (2, 'Manvi Gohil', 102, 'manvi@example.com', 'Electronics', 1);
INSERT INTO Students VALUES (3, 'Divya Patel', 103, 'divya@example.com', 'Chemistry', 2);

INSERT INTO Teachers VALUES (1, 'Prof. Patel', 'Computer Science');
INSERT INTO Teachers VALUES (2, 'Prof. Gohil', 'Electronics');
INSERT INTO Teachers VALUES (3, 'Prof. Shah', 'Chemistry');

INSERT INTO Subjects VALUES (1, 'Computer Science', 1);
INSERT INTO Subjects VALUES (2, 'Electronics', 2);
INSERT INTO Subjects VALUES (3, 'Chemistry', 3);

INSERT INTO Attendance VALUES (1, 1, 1, '2024-01-01', 'Present');
INSERT INTO Attendance VALUES (2, 2, 1, '2024-01-01', 'Present');

-- Query Results
SELECT * FROM Students;
SELECT * FROM Teachers;
""",

    "library_management": """-- Library Management System
CREATE TABLE Books (
  id INT PRIMARY KEY,
  title VARCHAR(255),
  author VARCHAR(255),
  isbn VARCHAR(50),
  available INT DEFAULT 1
);

CREATE TABLE Members (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(15)
);

CREATE TABLE Loans (
  id INT PRIMARY KEY,
  book_id INT,
  member_id INT,
  loan_date DATE,
  return_date DATE,
  FOREIGN KEY (book_id) REFERENCES Books(id),
  FOREIGN KEY (member_id) REFERENCES Members(id)
);

-- Sample Data
INSERT INTO Books VALUES (1, 'Python Programming', 'John Doe', '978-1234567890', 1);
INSERT INTO Books VALUES (2, 'Data Structures', 'Jane Smith', '978-0987654321', 1);

INSERT INTO Members VALUES (1, 'Meet Sutariya', 'meet@example.com', '9876543210');
INSERT INTO Members VALUES (2, 'Priya Shah', 'priya@example.com', '8765432109');

SELECT * FROM Books;
SELECT * FROM Members;
""",

    "employee_management": """-- Employee Management System
CREATE TABLE Employees (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  designation VARCHAR(100),
  department VARCHAR(100),
  salary DECIMAL(10, 2),
  hire_date DATE
);

CREATE TABLE Departments (
  id INT PRIMARY KEY,
  dept_name VARCHAR(100),
  manager_id INT
);

-- Sample Data
INSERT INTO Employees VALUES (1, 'Rajesh Kumar', 'Manager', 'IT', 75000.00, '2020-01-15');
INSERT INTO Employees VALUES (2, 'Sneha Patel', 'Developer', 'IT', 55000.00, '2021-03-10');
INSERT INTO Employees VALUES (3, 'Amit Shah', 'HR Executive', 'HR', 45000.00, '2019-07-20');

INSERT INTO Departments VALUES (1, 'IT', 1);
INSERT INTO Departments VALUES (2, 'HR', 3);

SELECT * FROM Employees;
SELECT * FROM Departments;
"""
}

# Gujarati to English keyword mapping
GUJARATI_KEYWORDS = {
    "કોલેજ": "college",
    "મેનેજમેન્ટ": "management",
    "લાઇબ્રેરી": "library",
    "પુસ્તકાલય": "library",
    "કર્મચારી": "employee",
    "સિસ્ટમ": "system"
}

def generate_sql_from_prompt(prompt):
    """
    Detects intent from prompt and returns appropriate SQL template
    """
    prompt_lower = prompt.lower()
    
    # Check for keywords
    if any(word in prompt_lower for word in ["કોલેજ", "college", "student"]):
        return SQL_TEMPLATES["college_management"], "કોલેજ મેનેજમેન્ટ સિસ્ટમ"
    
    elif any(word in prompt_lower for word in ["લાઇબ્રેરી", "library", "book", "પુસ્તકાલય"]):
        return SQL_TEMPLATES["library_management"], "લાઇબ્રેરી મેનેજમેન્ટ સિસ્ટમ"
    
    elif any(word in prompt_lower for word in ["કર્મચારી", "employee", "staff"]):
        return SQL_TEMPLATES["employee_management"], "કર્મચારી મેનેજમેન્ટ સિસ્ટમ"
    
    return None, None

if __name__ == "__main__":
    # Test
    code, name = generate_sql_from_prompt("કોલેજ મેનેજમેન્ટ સિસ્ટમ બનાવો")
    print(f"System: {name}")
    print(code)
