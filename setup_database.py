#!/usr/bin/env python3
"""
Standalone Database Setup Script for Bank Management System
Run this script to set up the complete database structure

Usage:
    python setup_database.py
    python setup_database.py --reset  # Reset and recreate all tables
    python setup_database.py --data   # Load sample data only
"""

import sys
import argparse
import mysql.connector
from mysql.connector import Error
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration (modify as needed)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Admin@12345',  # Change this to your MySQL password
    'port': 3306,
    'charset': 'utf8mb4',
    'autocommit': True
}

DATABASE_NAME = 'bank_management'

def check_mysql_connection():
    """Check if MySQL server is accessible"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info("✅ MySQL server connection successful")
            connection.close()
            return True
    except Error as e:
        logger.error(f"❌ MySQL server connection failed: {e}")
        logger.error("Please check:")
        logger.error("1. MySQL server is running")
        logger.error("2. Credentials are correct")
        logger.error("3. MySQL server is accessible on the specified host/port")
        return False

def create_database():
    """Create the database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DATABASE_NAME not in databases:
            logger.info(f"Creating database: {DATABASE_NAME}")
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"✅ Database '{DATABASE_NAME}' created successfully")
        else:
            logger.info(f"✅ Database '{DATABASE_NAME}' already exists")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        logger.error(f"❌ Error creating database: {e}")
        return False

def drop_all_tables():
    """Drop all existing tables (for reset)"""
    try:
        config_with_db = DB_CONFIG.copy()
        config_with_db['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config_with_db)
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Drop all tables
        for table in tables:
            logger.info(f"Dropping table: {table}")
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("✅ All tables dropped successfully")
        return True
        
    except Error as e:
        logger.error(f"❌ Error dropping tables: {e}")
        return False

def create_tables():
    """Create all required tables"""
    
    tables_sql = {
        'branches': """
            CREATE TABLE branches (
                branch_id INT AUTO_INCREMENT PRIMARY KEY,
                branch_code VARCHAR(10) UNIQUE NOT NULL,
                branch_name VARCHAR(100) NOT NULL,
                address VARCHAR(200) NOT NULL,
                city VARCHAR(50) NOT NULL,
                state VARCHAR(50) NOT NULL,
                pincode VARCHAR(10) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                email VARCHAR(100),
                manager_name VARCHAR(100),
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
                INDEX idx_branch_code (branch_code),
                INDEX idx_branch_city (city)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'customers': """
            CREATE TABLE customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_number VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                date_of_birth DATE NOT NULL,
                gender ENUM('MALE', 'FEMALE', 'OTHER') NOT NULL,
                phone VARCHAR(15) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE,
                address VARCHAR(200) NOT NULL,
                city VARCHAR(50) NOT NULL,
                state VARCHAR(50) NOT NULL,
                pincode VARCHAR(10) NOT NULL,
                pan_number VARCHAR(10) UNIQUE,
                aadhar_number VARCHAR(12) UNIQUE,
                annual_income DECIMAL(15,2),
                occupation VARCHAR(100),
                branch_id INT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED') DEFAULT 'ACTIVE',
                FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_customer_number (customer_number),
                INDEX idx_customer_phone (phone),
                INDEX idx_customer_email (email),
                INDEX idx_customer_pan (pan_number),
                INDEX idx_customer_branch (branch_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'accounts': """
            CREATE TABLE accounts (
                account_id INT AUTO_INCREMENT PRIMARY KEY,
                account_number VARCHAR(20) UNIQUE NOT NULL,
                customer_id INT NOT NULL,
                account_type ENUM('SAVINGS', 'CURRENT', 'FD', 'RD') NOT NULL,
                balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                opening_date DATE NOT NULL DEFAULT (CURDATE()),
                closing_date DATE NULL,
                interest_rate DECIMAL(5,2) NOT NULL DEFAULT 0.00,
                minimum_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                last_transaction_date TIMESTAMP NULL,
                status ENUM('ACTIVE', 'INACTIVE', 'CLOSED', 'FROZEN') DEFAULT 'ACTIVE',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_account_number (account_number),
                INDEX idx_account_customer (customer_id),
                INDEX idx_account_type (account_type),
                INDEX idx_account_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'transactions': """
            CREATE TABLE transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_number VARCHAR(20) UNIQUE NOT NULL,
                account_id INT NOT NULL,
                transaction_type ENUM('DEPOSIT', 'WITHDRAWAL', 'TRANSFER_IN', 'TRANSFER_OUT', 'INTEREST_CREDIT', 'FEE_DEBIT') NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                balance_before DECIMAL(15,2) NOT NULL,
                balance_after DECIMAL(15,2) NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                reference_account_id INT NULL,
                processed_by INT NULL,
                status ENUM('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'COMPLETED',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (reference_account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_transaction_number (transaction_number),
                INDEX idx_transaction_account (account_id),
                INDEX idx_transaction_date (transaction_date),
                INDEX idx_transaction_type (transaction_type),
                INDEX idx_transaction_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'loans': """
            CREATE TABLE loans (
                loan_id INT AUTO_INCREMENT PRIMARY KEY,
                loan_number VARCHAR(20) UNIQUE NOT NULL,
                customer_id INT NOT NULL,
                loan_type ENUM('PERSONAL', 'HOME', 'CAR', 'EDUCATION', 'BUSINESS') NOT NULL,
                principal_amount DECIMAL(15,2) NOT NULL,
                interest_rate DECIMAL(5,2) NOT NULL,
                tenure_months INT NOT NULL,
                emi_amount DECIMAL(15,2) NOT NULL,
                outstanding_amount DECIMAL(15,2) NOT NULL,
                disbursement_date DATE NULL,
                first_emi_date DATE NULL,
                last_payment_date DATE NULL,
                application_date DATE NOT NULL DEFAULT (CURDATE()),
                approval_date DATE NULL,
                approved_by INT NULL,
                purpose TEXT,
                collateral_details TEXT,
                status ENUM('APPLIED', 'APPROVED', 'DISBURSED', 'CLOSED', 'DEFAULTED') DEFAULT 'APPLIED',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_loan_number (loan_number),
                INDEX idx_loan_customer (customer_id),
                INDEX idx_loan_type (loan_type),
                INDEX idx_loan_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'loan_payments': """
            CREATE TABLE loan_payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                loan_id INT NOT NULL,
                payment_number INT NOT NULL,
                payment_date DATE NOT NULL,
                principal_amount DECIMAL(15,2) NOT NULL,
                interest_amount DECIMAL(15,2) NOT NULL,
                total_amount DECIMAL(15,2) NOT NULL,
                outstanding_balance DECIMAL(15,2) NOT NULL,
                payment_mode ENUM('CASH', 'CHEQUE', 'ONLINE', 'AUTO_DEBIT') DEFAULT 'CASH',
                reference_number VARCHAR(50),
                status ENUM('PAID', 'PENDING', 'OVERDUE', 'CANCELLED') DEFAULT 'PAID',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_payment_loan (loan_id),
                INDEX idx_payment_date (payment_date),
                INDEX idx_payment_status (status),
                UNIQUE KEY unique_loan_payment (loan_id, payment_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        'staff': """
            CREATE TABLE staff (
                staff_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                position VARCHAR(100) NOT NULL,
                branch_id INT NOT NULL,
                phone VARCHAR(15) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE,
                hire_date DATE NOT NULL,
                salary DECIMAL(10,2),
                status ENUM('ACTIVE', 'INACTIVE', 'TERMINATED') DEFAULT 'ACTIVE',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                INDEX idx_employee_id (employee_id),
                INDEX idx_staff_branch (branch_id),
                INDEX idx_staff_position (position)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    }
    
    try:
        config_with_db = DB_CONFIG.copy()
        config_with_db['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config_with_db)
        cursor = connection.cursor()
        
        # Create tables in order (respecting foreign key dependencies)
        table_order = ['branches', 'customers', 'accounts', 'transactions', 'loans', 'loan_payments', 'staff']
        
        for table_name in table_order:
            logger.info(f"Creating table: {table_name}")
            cursor.execute(tables_sql[table_name])
            logger.info(f"✅ Table '{table_name}' created successfully")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("✅ All tables created successfully")
        return True
        
    except Error as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False

def load_sample_data():
    """Load sample data into the database"""
    
    sample_data = {
        'branches': [
            ('BR001', 'Main Branch', '123 Bank Street', 'Mumbai', 'Maharashtra', '400001', '022-12345678', 'main@bankmail.com', 'John Manager'),
            ('BR002', 'Downtown Branch', '456 Finance Road', 'Delhi', 'Delhi', '110001', '011-87654321', 'downtown@bankmail.com', 'Jane Smith'),
            ('BR003', 'Tech Park Branch', '789 IT Boulevard', 'Bangalore', 'Karnataka', '560001', '080-11223344', 'techpark@bankmail.com', 'Tech Manager'),
            ('BR004', 'Commercial Branch', '321 Business District', 'Chennai', 'Tamil Nadu', '600001', '044-55667788', 'commercial@bankmail.com', 'Commerce Head'),
            ('BR005', 'Residential Branch', '654 Housing Colony', 'Pune', 'Maharashtra', '411001', '020-99887766', 'residential@bankmail.com', 'Resi Manager')
        ],
        
        'customers': [
            ('CUST001', 'Amit', 'Sharma', '1985-03-15', 'MALE', '9876543210', 'amit.sharma@email.com', '123 Green Avenue', 'Mumbai', 'Maharashtra', '400001', 'ABCDE1234F', '123456789012', 800000.00, 'Software Engineer', 1),
            ('CUST002', 'Priya', 'Patel', '1990-07-22', 'FEMALE', '9876543211', 'priya.patel@email.com', '456 Blue Street', 'Delhi', 'Delhi', '110001', 'FGHIJ5678K', '234567890123', 650000.00, 'Marketing Manager', 2),
            ('CUST003', 'Rajesh', 'Kumar', '1988-11-08', 'MALE', '9876543212', 'rajesh.kumar@email.com', '789 Red Colony', 'Bangalore', 'Karnataka', '560001', 'KLMNO9012P', '345678901234', 750000.00, 'Data Analyst', 3),
            ('CUST004', 'Sneha', 'Gupta', '1992-05-18', 'FEMALE', '9876543213', 'sneha.gupta@email.com', '321 Yellow Park', 'Chennai', 'Tamil Nadu', '600001', 'QRSTU3456V', '456789012345', 550000.00, 'Teacher', 4),
            ('CUST005', 'Vikram', 'Singh', '1987-09-12', 'MALE', '9876543214', 'vikram.singh@email.com', '654 Purple Lane', 'Pune', 'Maharashtra', '411001', 'WXYZ7890A', '567890123456', 900000.00, 'Business Owner', 5)
        ]
    }
    
    try:
        config_with_db = DB_CONFIG.copy()
        config_with_db['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config_with_db)
        cursor = connection.cursor()
        
        # Insert branches
        logger.info("Loading sample branches...")
        cursor.executemany("""
            INSERT INTO branches (branch_code, branch_name, address, city, state, pincode, phone, email, manager_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, sample_data['branches'])
        
        # Insert customers
        logger.info("Loading sample customers...")
        cursor.executemany("""
            INSERT INTO customers (customer_number, first_name, last_name, date_of_birth, gender, phone, email, address, city, state, pincode, pan_number, aadhar_number, annual_income, occupation, branch_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, sample_data['customers'])
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("✅ Sample data loaded successfully")
        return True
        
    except Error as e:
        logger.error(f"❌ Error loading sample data: {e}")
        return False

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='Bank Management System Database Setup')
    parser.add_argument('--reset', action='store_true', help='Reset and recreate all tables')
    parser.add_argument('--data', action='store_true', help='Load sample data only')
    
    args = parser.parse_args()
    
    logger.info("🚀 Bank Management System Database Setup")
    logger.info("=" * 50)
    
    # Check MySQL connection
    if not check_mysql_connection():
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Handle reset option
    if args.reset:
        logger.info("🔄 Resetting database (dropping all tables)...")
        if not drop_all_tables():
            sys.exit(1)
    
    # Create tables (unless only loading data)
    if not args.data:
        if not create_tables():
            sys.exit(1)
    
    # Load sample data
    if args.data or not args.reset:
        load_sample_data()
    
    logger.info("🎉 Database setup completed successfully!")
    logger.info("=" * 50)
    logger.info("You can now run the main application: python main.py")

if __name__ == "__main__":
    main()
