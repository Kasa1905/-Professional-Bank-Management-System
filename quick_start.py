"""
Quick Start Guide for Bank Management System
Run this script to quickly set up and test the application
"""

import os
import sys
from pathlib import Path

def quick_setup():
    """Quick setup for development/testing"""
    print("=" * 50)
    print("  BANK MANAGEMENT SYSTEM - QUICK START")
    print("=" * 50)
    
    # Create basic directories
    dirs = ["logs", "exports", "backups", "temp"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created/verified directory: {dir_name}")
    
    # Check if config.py exists
    if not Path("config.py").exists():
        print("\n⚠️  config.py not found. Creating template...")
        create_config_template()
    else:
        print("✓ Configuration file found")
    
    print("\nQuick setup complete!")
    print("\nTo run the application:")
    print("1. Install dependencies: pip install mysql-connector-python pandas openpyxl reportlab")
    print("2. Update config.py with your MySQL credentials")
    print("3. Run: python main.py")
    
    print("\nTo setup database:")
    print("1. Create MySQL database: bank_management")
    print("2. Execute: database/schema.sql")
    print("3. Execute: database/sample_data.sql")

def create_config_template():
    """Create a basic config template"""
    config_content = '''# Database Configuration - Update with your MySQL details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "bank_management",
    "charset": "utf8mb4",
    "autocommit": True
}

# Account Types and Settings
ACCOUNT_TYPES = ["Savings", "Current", "Fixed Deposit", "Recurring Deposit"]
MIN_BALANCE = {"Savings": 1000.0, "Current": 5000.0, "Fixed Deposit": 10000.0, "Recurring Deposit": 500.0}
INTEREST_RATES = {"Savings": 4.0, "Current": 0.0, "Fixed Deposit": 6.5, "Recurring Deposit": 5.5}
LOAN_RATES = {"Personal": 12.0, "Home": 8.5, "Car": 10.0, "Education": 7.5, "Business": 11.0}

# Application Settings
APP_TITLE = "Bank Management System"
APP_VERSION = "1.0.0"
'''
    
    with open("config.py", "w") as f:
        f.write(config_content)
    print("✓ Created config.py template")

if __name__ == "__main__":
    quick_setup()
