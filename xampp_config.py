# XAMPP Database Configuration for Bankoo AI

# MySQL Connection Settings
XAMPP_MYSQL_HOST = "localhost"
XAMPP_MYSQL_PORT = 3306
XAMPP_MYSQL_USER = "root"
XAMPP_MYSQL_PASSWORD = ""  # Default XAMPP has no root password

# XAMPP Executable Paths
XAMPP_ROOT = r"C:\xampp"
XAMPP_PHP_PATH = r"C:\xampp\php\php.exe"
XAMPP_MYSQL_PATH = r"C:\xampp\mysql\bin\mysql.exe"
XAMPP_APACHE_PATH = r"C:\xampp\apache\bin\httpd.exe"

# Web Server URLs
PHPMYADMIN_URL = "http://localhost/phpmyadmin"
LOCALHOST_URL = "http://localhost"

# Database Settings
DEFAULT_DB = "bankoo_db"  # Default database name for Bankoo projects
DB_CHARSET = "utf8mb4"
DB_COLLATION = "utf8mb4_general_ci"

def get_mysql_connection():
    """
    Get a MySQL connection using XAMPP settings
    Requires: pip install mysql-connector-python
    """
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host=XAMPP_MYSQL_HOST,
            port=XAMPP_MYSQL_PORT,
            user=XAMPP_MYSQL_USER,
            password=XAMPP_MYSQL_PASSWORD,
            charset=DB_CHARSET
        )
        return connection
    except ImportError:
        print("⚠️ mysql-connector-python not installed")
        print("Run: pip install mysql-connector-python")
        return None
    except Exception as e:
        print(f"❌ MySQL Connection Error: {e}")
        print("Make sure XAMPP MySQL is running!")
        return None

def test_connection():
    """Test XAMPP MySQL connection"""
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Connected to MySQL {version[0]}")
        cursor.close()
        conn.close()
        return True
    return False

if __name__ == "__main__":
    print("Testing XAMPP MySQL Connection...")
    test_connection()
