@echo off
setlocal EnableDelayedExpansion
echo ============================================================
echo   BANKOO AI - ULTIMATE LANGUAGE VERIFIER (14/14)
echo ============================================================
echo.
echo Setting up Precision Environment...

REM --- PATH INJECTION (Order Matters!) ---
REM 1. Java 17 
set "PATH=C:\Program Files\Java\jdk-17.0.12\bin;%PATH%"
REM 2. LLVM (C/C++) - ADDING QUOTES NOT NEEDED IN PATH VAR BUT SPACES MATTER
set "PATH=C:\Program Files\LLVM\bin;%PATH%"
REM 3. Rust (Cargo)
set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
REM 4. Git (Bash)
set "PATH=C:\Program Files\Git\bin;%PATH%"

echo.
echo [DEBUG] Path Check:
where java
where clang
where rustc

echo.
echo Running Hello World test for EVERY language...
echo.

if not exist "test_sandbox" mkdir test_sandbox
cd test_sandbox

REM --- 1. PYTHON ---
echo [1/14] Python...
echo print("Hello from Python!") > test.py
python test.py > nul
if %errorlevel%==0 (echo   [YES] Python Working) else (echo   [NO] Python FAILED)

REM --- 2. JAVASCRIPT (Node) ---
echo [2/14] Node.js...
echo console.log("Hello from Node!"); > test.js
node test.js > nul
if %errorlevel%==0 (echo   [YES] Node.js Working) else (echo   [NO] Node.js FAILED)

REM --- 3. JAVA ---
echo [3/14] Java...
echo public class Test { public static void main(String[] args) { System.out.println("Hello from Java!"); } } > Test.java
javac Test.java > nul 2>&1
if %errorlevel%==0 (
    java Test > nul
    if !errorlevel!==0 (echo   [YES] Java Working) else (echo   [NO] Java Run Failed)
) else (echo   [NO] Java Compile Failed)

REM --- 4. C (Clang) ---
echo [4/14] C (Clang)...
echo #include ^<stdio.h^> > test.c
echo int main() { printf("Hello from C!"); return 0; } >> test.c
REM Using direct call with quotes for path safety
"C:\Program Files\LLVM\bin\clang.exe" test.c -o test_c.exe > nul 2>&1
if %errorlevel%==0 (
    test_c.exe > nul
    if !errorlevel!==0 (echo   [YES] C Clang Working) else (echo   [NO] C Run Failed)
) else (echo   [NO] C Compile Failed)

REM --- 5. C++ (Clang++) ---
echo [5/14] C++ (Clang++)...
echo #include ^<iostream^> > test.cpp
echo int main() { std::cout ^<^< "Hello from C++!"; return 0; } >> test.cpp
"C:\Program Files\LLVM\bin\clang++.exe" test.cpp -o test_cpp.exe > nul 2>&1
if %errorlevel%==0 (
    test_cpp.exe > nul
    if !errorlevel!==0 (echo   [YES] C++ Working) else (echo   [NO] C++ Run Failed)
) else (echo   [NO] C++ Compile Failed)

REM --- 6. PHP ---
echo [6/14] PHP...
echo ^<?php echo "Hello from PHP!"; ?^> > test.php
php test.php > nul 2>&1
if %errorlevel%==0 (echo   [YES] PHP Working) else (echo   [NO] PHP FAILED)

REM --- 7. GO ---
echo [7/14] Go...
echo package main; import "fmt"; func main() { fmt.Println("Hello from Go!") } > test.go
go run test.go > nul 2>&1
if %errorlevel%==0 (echo   [YES] Go Working) else (echo   [NO] Go FAILED)

REM --- 8. RUST ---
echo [8/14] Rust...
echo fn main() { println!("Hello from Rust!"); } > test.rs
"%USERPROFILE%\.cargo\bin\rustc.exe" test.rs -o test_rust.exe > nul 2>&1
if %errorlevel%==0 (
    test_rust.exe > nul
    if !errorlevel!==0 (echo   [YES] Rust Working) else (echo   [NO] Rust Run Failed)
) else (echo   [NO] Rust Compile Failed)

REM --- 9. RUBY ---
echo [9/14] Ruby...
echo puts "Hello from Ruby!" > test.rb
ruby test.rb > nul 2>&1
if %errorlevel%==0 (echo   [YES] Ruby Working) else (echo   [NO] Ruby FAILED)

REM --- 10. TYPESCRIPT ---
echo [10/14] TypeScript...
echo console.log("Hello from TS!"); > test.ts
call tsc test.ts > nul 2>&1
if %errorlevel%==0 (
    node test.js > nul
    if !errorlevel!==0 (echo   [YES] TypeScript Working) else (echo   [NO] TypeScript Run Failed)
) else (echo   [NO] TypeScript Compile Failed)

REM --- 11. C# (.NET) ---
echo [11/14] C# (.NET)...
dotnet --version > nul 2>&1
if %errorlevel%==0 (echo   [YES] DotNet C# Working) else (echo   [NO] C# FAILED)

REM --- 12. R (RScript) ---
echo [12/14] R...
echo cat("Hello from R!") > test.R
Rscript test.R > nul 2>&1
if %errorlevel%==0 (echo   [YES] R Working) else (echo   [NO] R FAILED)

REM --- 13. BASH ---
echo [13/14] Bash...
echo echo "Hello from Bash!" > test.sh
bash test.sh > nul 2>&1
if %errorlevel%==0 (echo   [YES] Bash Working) else (echo   [NO] Bash FAILED)

REM --- 14. SQL ---
echo [14/14] SQL (MySQL Client)...
mysql --version > nul 2>&1
if %errorlevel%==0 (echo   [YES] MySQL Working) else (echo   [NO] MySQL FAILED)

echo.
echo ============================================================
echo   VERIFICATION COMPLETE
echo ============================================================
echo.
echo clean up...
cd ..
rmdir /s /q test_sandbox
pause
