"""
Installation and Setup Script for Bank Management System
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("    BANK MANAGEMENT SYSTEM - INSTALLATION SCRIPT")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("\nInstalling required packages...")
    
    requirements = [
        "mysql-connector-python>=8.0.0"
    ]
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating project directories...")
    
    directories = [
        "logs",
        "backups",
        "exports",
        "temp"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_mysql_connection():
    """Check MySQL server availability"""
    print("\nChecking MySQL connection...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        # Try to connect to MySQL server
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            print("✅ MySQL server connection successful")
            connection.close()
            return True
        
    except ImportError:
        print("❌ mysql-connector-python not installed")
        return False
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        print("Please check your MySQL server and credentials in config.py")
        return False

def create_database():
    """Create database if it doesn't exist"""
    print("\nCreating database...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created/verified")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database creation failed: {str(e)}")
        return False

def setup_database_schema():
    """Setup database schema"""
    print("\nSetting up database schema...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Read and execute schema.sql
        with open('database/schema.sql', 'r') as file:
            schema_sql = file.read()
        
        # Split and execute individual statements
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print("✅ Database schema created successfully")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema setup failed: {str(e)}")
        return False

def load_sample_data():
    """Load sample data"""
    print("\nLoading sample data...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Read and execute sample_data.sql
        with open('database/sample_data.sql', 'r') as file:
            sample_sql = file.read()
        
        # Split and execute individual statements
        statements = sample_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print("✅ Sample data loaded successfully")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Sample data loading failed: {str(e)}")
        return False

def create_config_file():
    """Create config file if it doesn't exist"""
    config_path = Path("config.py")
    
    if not config_path.exists():
        print("\nCreating default config file...")
        
        config_content = '''"""
Database Configuration for Bank Management System
Update the credentials below according to your MySQL setup
"""

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password_here",
    "database": "bank_management",
    "charset": "utf8mb4",
    "autocommit": True
}

# Account Types
ACCOUNT_TYPES = ["Savings", "Current", "Fixed Deposit", "Recurring Deposit"]

# Minimum Balance Requirements
MIN_BALANCE = {
    "Savings": 1000.0,
    "Current": 5000.0,
    "Fixed Deposit": 10000.0,
    "Recurring Deposit": 500.0
}

# Interest Rates (Annual %)
INTEREST_RATES = {
    "Savings": 4.0,
    "Current": 0.0,
    "Fixed Deposit": 6.5,
    "Recurring Deposit": 5.5
}

# Loan Interest Rates (Annual %)
LOAN_RATES = {
    "Personal": 12.0,
    "Home": 8.5,
    "Car": 10.0,
    "Education": 7.5,
    "Business": 11.0
}

# Application Settings
APP_TITLE = "Bank Management System"
APP_VERSION = "1.0.0"
'''
        
        with open(config_path, 'w') as file:
            file.write(config_content)
        
        print("✅ Default config file created")
        print("⚠️  Please update the database credentials in config.py")
        return False  # Return False to indicate manual configuration needed
    
    return True

def verify_installation():
    """Verify installation by testing imports"""
    print("\nVerifying installation...")
    
    try:
        # Test basic imports (only the ones we actually use)
        import mysql.connector
        print("✅ mysql-connector-python imported successfully")
        
        # Test our core modules
        from models.customer import Customer
        from models.account import Account
        from models.transaction import Transaction
        print("✅ All project modules imported successfully")
        
        # Test GUI modules
        from gui.customer_window import CustomerWindow
        from gui.account_window import AccountWindow
        from gui.transaction_window import TransactionWindow
        from gui.reports_window import ReportsWindow
        print("✅ All GUI modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("    INSTALLATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update database credentials in config.py")
    print("2. Ensure MySQL server is running")
    print("3. Run the application with: python main.py")
    print("\nProject Structure:")
    print("├── main.py              # Application entry point")
    print("├── config.py            # Database configuration")
    print("├── models/              # Database models")
    print("├── gui/                 # GUI components")
    print("├── database/            # SQL scripts")
    print("├── utils/               # Utility functions")
    print("├── logs/                # Application logs")
    print("└── exports/             # Generated reports")
    print("\nFor help and documentation, check README.md")
    print("=" * 60)

def main():
    """Main installation function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create config file
    config_exists = create_config_file()
    
    # Install requirements
    if not install_requirements():
        print("❌ Package installation failed")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # If config exists, try database operations
    if config_exists:
        if check_mysql_connection():
            if create_database():
                if setup_database_schema():
                    load_sample_data()
    
    # Verify installation
    verify_installation()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
