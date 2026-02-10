# Bankoo AI - Complete Runtime Environment Setup Guide

## 📦 Language Runtimes & Software Installation

This guide helps you install the necessary software/compilers for each programming language supported by Bankoo AI.

---

## ✅ Currently Installed (via Python)

These work **immediately** after installing Python:
- ✅ **Python** - Already installed
- ✅ **SQL (SQLite)** - Built into Python
- ✅ **HTML** - Runs in browser, no installation needed

---

## 🔧 Languages Requiring Additional Software

### 1. **JavaScript / Node.js**
**Download:** https://nodejs.org/
**Version:** LTS (Long Term Support)
**Install:** Run installer → Check "Add to PATH"
**Verify:** Open CMD and run: `node --version`

---

### 2. **Java (JDK)**
**Download:** https://www.oracle.com/java/technologies/downloads/
**Alternative:** https://adoptium.net/ (Open Source)
**Version:** JDK 17 or newer
**Install:** Run installer → Set JAVA_HOME environment variable
**Verify:** `java --version` and `javac --version`

---

### 3. **C / C++ (GCC via MinGW)**
**Download:** https://sourceforge.net/projects/mingw-w64/
**Alternative:** Install Visual Studio Community (comes with MSVC)
**Install:** 
- Download MinGW installer
- Select: gcc-core, g++, mingw32-make
- Add `C:\MinGW\bin` to PATH
**Verify:** `gcc --version` and `g++ --version`

---

### 4. **C# (.NET SDK)**
**Download:** https://dotnet.microsoft.com/download
**Version:** .NET 8.0 (latest)
**Install:** Run installer
**Verify:** `dotnet --version`

---

### 5. **Go (Golang)**
**Download:** https://go.dev/dl/
**Version:** Latest stable
**Install:** Run installer → Automatically adds to PATH
**Verify:** `go version`

---

### 6. **Rust**
**Download:** https://www.rust-lang.org/tools/install
**Install:** 
- Download rustup-init.exe
- Run and follow prompts
- Installs: cargo, rustc, rust-analyzer
**Verify:** `rustc --version` and `cargo --version`

---

### 7. **PHP (via XAMPP - RECOMMENDED)**
**Download:** https://www.apachefriends.org/download.html
**Version:** Latest (includes PHP 8.2+, MySQL, Apache)
**Install:** 
- Run XAMPP installer
- Select: Apache, MySQL, PHP, phpMyAdmin
- Install to `C:\xampp`
- Add `C:\xampp\php` to PATH
**Verify:** `php --version`

**After Installation:**
- Open XAMPP Control Panel
- Start Apache and MySQL services
- Access phpMyAdmin: http://localhost/phpmyadmin

---

### 8. **Ruby**
**Download:** https://rubyinstaller.org/downloads/
**Version:** Ruby+Devkit 3.2.x
**Install:** Run installer → Check "Add to PATH"
**Verify:** `ruby --version`

---

### 9. **TypeScript**
**Pre-requisite:** Install Node.js first (see #1)
**Install:** Open CMD and run:
```bash
npm install -g typescript ts-node
```
**Verify:** `tsc --version`

---

### 10. **Bash (Git Bash for Windows)**
**Download:** https://git-scm.com/download/win
**Install:** 
- Run installer
- Select "Git Bash Here" option
- Adds bash shell to Windows
**Verify:** Open Git Bash and run: `bash --version`

---

### 11. **R Programming**
**Download:** https://cran.r-project.org/bin/windows/base/
**Alternative:** https://posit.co/download/rstudio-desktop/ (RStudio IDE)
**Install:** Run installer
**Verify:** `R --version`

---

## 🎯 Quick Installation Priority

### **Tier 1 - Essential (Install First)**
1. **Node.js** - For JavaScript/TypeScript
2. **Java JDK** - For Java
3. **XAMPP** - For PHP + MySQL

### **Tier 2 - Common Use**
4. **MinGW (C/C++)** - For C/C++
5. **.NET SDK** - For C#
6. **Go** - For Golang

### **Tier 3 - Advanced**
7. **Rust**
8. **Ruby**
9. **R**
10. **Git Bash** - For Bash scripts

---

## 🔗 XAMPP Integration with Bankoo AI

### **Setup Steps:**

1. **Install XAMPP** (if not already):
   - Download from https://www.apachefriends.org/
   - Install to `C:\xampp`

2. **Add PHP to System PATH:**
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit PATH → Add `C:\xampp\php`

3. **Configure Bankoo to Use XAMPP MySQL:**

Create this file: `c:\Users\Meet Sutariya\Desktop\final banko.ai\xampp_config.py`

```python
# XAMPP Database Configuration for Bankoo AI
XAMPP_MYSQL_HOST = "localhost"
XAMPP_MYSQL_PORT = 3306
XAMPP_MYSQL_USER = "root"
XAMPP_MYSQL_PASSWORD = ""  # Default XAMPP has no password
XAMPP_PHP_PATH = r"C:\xampp\php\php.exe"
XAMPP_MYSQL_PATH = r"C:\xampp\mysql\bin\mysql.exe"
```

4. **Access phpMyAdmin:**
   - Start XAMPP Control Panel
   - Click "Start" for Apache and MySQL
   - Open browser: http://localhost/phpmyadmin
   - Create databases and tables visually!

5. **Run PHP with Database:**
Now you can write PHP code in Bankoo that connects to XAMPP MySQL:

```php
<?php
$conn = new mysqli("localhost", "root", "", "test_db");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected to XAMPP MySQL successfully!";
$conn->close();
?>
```

---

## 🚀 Auto-Detection Script

I'll create a script that checks which language runtimes are installed!

See: `CHECK_RUNTIMES.bat`

---

## 📋 Installation Checklist

Use this to track your progress:

- [ ] Python (Already installed ✅)
- [ ] Node.js + npm
- [ ] Java JDK
- [ ] XAMPP (PHP + MySQL + Apache)
- [ ] C/C++ (MinGW or Visual Studio)
- [ ] .NET SDK (C#)
- [ ] Go (Golang)
- [ ] Rust
- [ ] Ruby
- [ ] TypeScript (requires Node.js)
- [ ] Git Bash
- [ ] R

---

## 💡 Pro Tips

1. **Install in Order:** Start with Tier 1, then move to Tier 2/3 based on your needs
2. **Restart After Installation:** Some software requires a system restart to update PATH
3. **Verify Each Install:** Use the verification commands to confirm success
4. **XAMPP First:** If you need PHP/MySQL, install XAMPP before anything else

---

## 🔍 After Installation

Run `CHECK_RUNTIMES.bat` to see which languages are ready to use in Bankoo AI!

The script will show:
- ✅ Green = Installed and working
- ❌ Red = Not installed or not in PATH
- ⚠️ Yellow = Partial installation (needs configuration)

---

**Questions?** Check the `FEATURE_GUIDE.md` or run the runtime checker script!
