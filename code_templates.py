"""
Bankoo AI - Multi-Language Code Generator
Generates code templates for 14 languages based on natural language prompts
"""

TEMPLATES = {
    # --- PYTHON (Deep GUI & Automation) ---
    "python": {
        "calculator": """import tkinter as tk
from math import sqrt, pow, log10

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bankoo Scientific Calculator")
        self.root.geometry("400x600")
        self.entry = tk.Entry(root, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
            'sqrt', 'pow', 'log', '.' 
        ]
        
        row = 1
        col = 0
        for btn in buttons:
            cmd = lambda x=btn: self.click(x)
            tk.Button(root, text=btn, padx=20, pady=20, font=("Arial", 14), command=cmd).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, key):
        if key == "=":
            try:
                result = str(eval(self.entry.get()))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif key == "C":
            self.entry.delete(0, tk.END)
        elif key == "sqrt":
            try:
                val = float(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(sqrt(val)))
            except: self.entry.insert(tk.END, "Err")
        else:
            self.entry.insert(tk.END, key)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()""",

        "server": """from flask import Flask, jsonify, request
app = Flask(__name__)

# Bankoo Microservice Demo
data_store = {"users": [], "logs": []}

@app.route('/')
def home():
    return jsonify({"status": "active", "system": "Bankoo AI Core"})

@app.route('/api/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        user = request.json
        data_store['users'].append(user)
        return jsonify({"msg": "User added", "count": len(data_store['users'])})
    return jsonify(data_store['users'])

if __name__ == '__main__':
    print("Starting Flask Microservice on port 5000...")
    app.run(debug=True, port=5000)""",

        "hello": """print("Hello from Bankoo AI - Advanced Python Context")
# Demonstrating List Comprehensions and Classes
class Greeter:
    def __init__(self, name): self.name = name
    def say(self): return f"Greetings, {self.name}!"

people = ["Rahul", "Priya", "Amit"]
greetings = [Greeter(p).say() for p in people]
print("\\n".join(greetings))"""
    },

    # --- JAVA (Enterprise OOP) ---
    "java": {
        "hello": """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Bankoo Java Runtime!");
        System.out.println("JVM Version: " + System.getProperty("java.version"));
    }
}""",
        "college": """import java.util.ArrayList;
import java.util.List;

// Deep Object-Oriented College System
class Student {
    private String name;
    private int id;
    
    public Student(String name, int id) {
        this.name = name;
        this.id = id;
    }
    
    public void display() {
        System.out.println("ID: " + id + " | Name: " + name);
    }
}

class Department {
    private String deptName;
    private List<Student> students = new ArrayList<>();
    
    public Department(String name) { this.deptName = name; }
    
    public void enroll(Student s) { students.add(s); }
    
    public void showAll() {
        System.out.println("Department: " + deptName);
        for(Student s : students) s.display();
    }
}

public class CollegeSystem {
    public static void main(String[] args) {
        Department cs = new Department("Computer Science");
        cs.enroll(new Student("Arvind", 101));
        cs.enroll(new Student("Priya", 102));
        cs.showAll();
    }
}"""
    },

    # --- C++ (Systems Programming) ---
    "cpp": {
        "hello": """#include <iostream>
#include <vector>
#include <string>

// Advanced C++ Demo
class Logger {
public:
    static void log(const std::string& msg) {
        std::cout << "[LOG]: " << msg << std::endl;
    }
};

int main() {
    Logger::log("Bankoo C++ System Init...");
    std::vector<int> data = {1, 2, 3, 4, 5};
    
    for(const auto& val : data) {
        std::cout << "Processing: " << val * 2 << std::endl;
    }
    return 0;
}""",
        "matrix": """#include <iostream>
using namespace std;

// Matrix Multiplication Logic
int main() {
    int r1=2, c1=2, r2=2, c2=2;
    int m1[2][2] = {{1,2}, {3,4}};
    int m2[2][2] = {{5,6}, {7,8}};
    int result[2][2] = {0};

    cout << "Multiplying 2x2 Matrices..." << endl;

    for(int i=0; i<r1; ++i)
        for(int j=0; j<c2; ++j)
            for(int k=0; k<c1; ++k)
                result[i][j] += m1[i][k] * m2[k][j];

    cout << "Result Matrix:" << endl;
    for(int i=0; i<r1; ++i) {
        for(int j=0; j<c2; ++j)
            cout << result[i][j] << " ";
        cout << endl;
    }
    return 0;
}"""
    },

    # --- JAVASCRIPT / NODE (Backend API) ---
    "javascript": {
        "server": """const http = require('http');

// Simple Bankoo REST API
const users = [
    { id: 1, name: 'Meet', role: 'Admin' },
    { id: 2, name: 'User', role: 'Guest' }
];

const server = http.createServer((req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');

    if (req.url === '/api/users' && req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify(users));
    } else {
        res.writeHead(404);
        res.end(JSON.stringify({ error: 'Route not found' }));
    }
});

server.listen(3000, () => {
    console.log('🚀 Bankoo Node API running on http://localhost:3000');
});"""
    },

    # --- GO (Concurrency) ---
    "go": {
        "server": """package main
import (
    "fmt"
    "net/http"
    "time"
)

func worker(id int) {
    fmt.Printf("Worker %d started\\n", id)
    time.Sleep(time.Second)
    fmt.Printf("Worker %d finished\\n", id)
}

func main() {
    // Goroutines Demo
    fmt.Println("Main started...")
    for i := 1; i <= 3; i++ {
        go worker(i)
    }
    
    // Simple Web Server
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from Bankoo Go Server!")
    })
    
    fmt.Println("Server listening on :8080")
    // Keep main alive for goroutines if using ListenAndServe
    http.ListenAndServe(":8080", nil)
}"""
    },

    # --- RUST (Safety) ---
    "rust": {
        "hello": """struct User {
    username: String,
    active: bool,
}

fn main() {
    println!("--- Bankoo Rust System ---");
    
    let user1 = User {
        username: String::from("meet_admin"),
        active: true,
    };
    
    if user1.active {
        println!("User {} is ONLINE", user1.username);
    } else {
        println!("User {} is OFFLINE", user1.username);
    }
    
    // Vector Memory Safety Demo
    let mut v = vec![1, 2, 3];
    v.push(4);
    println!("Vector Data: {:?}", v);
}"""
    },

    # --- PHP ---
    "php": {
        "hello": """<?php
echo "Hello from Bankoo PHP!";
$x = 10;
$y = 20;
echo "\\nSum: " . ($x + $y);
?>"""
    },

    # --- C# ---
    "csharp": {
        "hello": """using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello from C# (.NET)!");
    }
}"""
    },

    # --- RUBY ---
    "ruby": {
        "hello": """puts "Hello from Ruby!"
x = 10
y = 20
puts "Sum is #{x + y}"
"""
    },

    # --- R LANGUAGE ---
    "r": {
        "hello": """print("Hello from R Language!")
x <- 10
y <- 20
print(paste("Sum is:", x + y))
"""
    },

    # --- TYPESCRIPT ---
    "typescript": {
        "hello": """let message: string = "Hello from TypeScript!";
console.log(message);"""
    },

    # --- BASH ---
    "bash": {
        "hello": """#!/bin/bash
echo "Hello from Bash Script!"
echo "Current Directory: $PWD"
"""
    },
    
    # --- SQL ---
    "sql": {
        "hello": """-- Creates a simple table
CREATE TABLE Demo (id INT, message TEXT);
INSERT INTO Demo VALUES (1, 'Hello SQL');
SELECT * FROM Demo;""",

        "college": """-- College Management System
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

INSERT INTO Teachers VALUES (1, 'Prof. Patel', 'Computer Science');
INSERT INTO Teachers VALUES (2, 'Prof. Gohil', 'Electronics');

INSERT INTO Subjects VALUES (1, 'Computer Science', 1);
INSERT INTO Subjects VALUES (2, 'Electronics', 2);

INSERT INTO Attendance VALUES (1, 1, 1, '2024-01-01', 'Present');

SELECT * FROM Students;
SELECT * FROM Teachers;""",

        "library": """-- Library Management System
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

INSERT INTO Books VALUES (1, 'Python Programming', 'John Doe', '978-1234567890', 1);
INSERT INTO Members VALUES (1, 'Meet Sutariya', 'meet@example.com', '9876543210');
INSERT INTO Loans VALUES (1, 1, 1, '2024-01-01', '2024-01-15');

SELECT * FROM Books;
SELECT * FROM Loans;"""
    }
}

GUJARATI_MAPPING = {
    "calculator": ["calculator", "ગણતરી", "કેલ્ક્યુલેટર"],
    "hello": ["hello", "નમસ્તે", "હાય", "sample", "test"],
    "server": ["server", "સર્વર", "api"],
    "college": ["college", "કોલેજ", "વિદ્યાર્થી", "student"],
    "library": ["library", "પુસ્તકાલય", "book", "લાઇબ્રેરી"]
}

def generate_code(prompt, language="python"):
    lang_key = language.lower()
    
    # Map common aliases
    if lang_key in ["js", "node"]: lang_key = "javascript"
    if lang_key in ["py"]: lang_key = "python"
    if lang_key in ["ts"]: lang_key = "typescript"
    if lang_key in ["c++"]: lang_key = "cpp"
    if lang_key in ["cs", "c#.net"]: lang_key = "csharp"

    if lang_key not in TEMPLATES:
        return f"# Sorry, no templates for {language} yet.", "unknown"

    # Detect intent from prompt (Naive keyword search)
    prompt_lower = prompt.lower()
    selected_template = "hello" # Default

    for key, keywords in GUJARATI_MAPPING.items():
        if any(w in prompt_lower for w in keywords):
            if key in TEMPLATES[lang_key]:
                selected_template = key
                break
    
    return TEMPLATES[lang_key].get(selected_template, TEMPLATES[lang_key]["hello"]), selected_template


if __name__ == "__main__":
    import sys
    # Demo
    if len(sys.argv) > 2:
        lang = sys.argv[1]
        prmt = sys.argv[2]
        print(generate_code(prmt, lang))
    else:
        print("Usage: python code_templates.py [language] [prompt]")
        print("Example: python code_templates.py python calculator")
