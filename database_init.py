"""
Database Initialization and Auto-Setup Module
Automatically creates database and tables if they don't exist
"""

import mysql.connector
from mysql.connector import Error
import logging
from config import DB_CONFIG
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """Handles automatic database and table creation"""
    
    def __init__(self):
        self.db_config = DB_CONFIG.copy()
        self.database_name = self.db_config.pop('database')
        
    def check_and_create_database(self):
        """Check if database exists, create if missing"""
        try:
            # Connect without specifying database
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if self.database_name not in databases:
                logger.info(f"Database '{self.database_name}' not found. Creating...")
                cursor.execute(f"CREATE DATABASE {self.database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                logger.info(f"✅ Database '{self.database_name}' created successfully")
            else:
                logger.info(f"✅ Database '{self.database_name}' already exists")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Error checking/creating database: {e}")
            return False
    
    def get_existing_tables(self):
        """Get list of existing tables in the database"""
        try:
            # Connect to the specific database
            full_config = DB_CONFIG.copy()
            connection = mysql.connector.connect(**full_config)
            cursor = connection.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            cursor.close()
            connection.close()
            return tables
            
        except Error as e:
            logger.error(f"❌ Error getting existing tables: {e}")
            return []
    
    def get_required_tables(self):
        """Define all required tables and their creation SQL"""
        return {
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
    
    def create_missing_tables(self):
        """Create any missing tables"""
        try:
            # Get existing and required tables
            existing_tables = self.get_existing_tables()
            required_tables = self.get_required_tables()
            
            # Find missing tables
            missing_tables = [table for table in required_tables.keys() if table not in existing_tables]
            
            if not missing_tables:
                logger.info("✅ All required tables already exist")
                return True
            
            logger.info(f"Creating missing tables: {missing_tables}")
            
            # Connect to database
            full_config = DB_CONFIG.copy()
            connection = mysql.connector.connect(**full_config)
            cursor = connection.cursor()
            
            # Create missing tables in order (respecting foreign key dependencies)
            table_order = ['branches', 'customers', 'accounts', 'transactions', 'loans', 'loan_payments', 'staff']
            
            for table_name in table_order:
                if table_name in missing_tables:
                    logger.info(f"Creating table: {table_name}")
                    cursor.execute(required_tables[table_name])
                    logger.info(f"✅ Table '{table_name}' created successfully")
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info("✅ All missing tables created successfully")
            return True
            
        except Error as e:
            logger.error(f"❌ Error creating tables: {e}")
            return False
    
    def create_triggers(self):
        """Create useful triggers for the database"""
        triggers = {
            'update_account_balance_after_transaction': """
                CREATE TRIGGER IF NOT EXISTS update_account_balance_after_transaction
                AFTER INSERT ON transactions
                FOR EACH ROW
                BEGIN
                    UPDATE accounts 
                    SET balance = NEW.balance_after,
                        last_transaction_date = NEW.transaction_date
                    WHERE account_id = NEW.account_id;
                END
            """,
            
            'prevent_negative_balance': """
                CREATE TRIGGER IF NOT EXISTS prevent_negative_balance
                BEFORE INSERT ON transactions
                FOR EACH ROW
                BEGIN
                    DECLARE current_balance DECIMAL(15,2);
                    
                    SELECT balance INTO current_balance 
                    FROM accounts 
                    WHERE account_id = NEW.account_id;
                    
                    IF NEW.transaction_type IN ('WITHDRAWAL', 'TRANSFER_OUT', 'FEE_DEBIT') 
                       AND current_balance < NEW.amount THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Insufficient balance for transaction';
                    END IF;
                END
            """,
            
            'update_loan_outstanding': """
                CREATE TRIGGER IF NOT EXISTS update_loan_outstanding
                AFTER INSERT ON loan_payments
                FOR EACH ROW
                BEGIN
                    UPDATE loans 
                    SET outstanding_amount = NEW.outstanding_balance,
                        last_payment_date = NEW.payment_date,
                        status = CASE 
                            WHEN NEW.outstanding_balance <= 0 THEN 'CLOSED'
                            ELSE status
                        END
                    WHERE loan_id = NEW.loan_id;
                END
            """
        }
        
        try:
            full_config = DB_CONFIG.copy()
            connection = mysql.connector.connect(**full_config)
            cursor = connection.cursor()
            
            for trigger_name, trigger_sql in triggers.items():
                try:
                    cursor.execute(trigger_sql)
                    logger.info(f"✅ Trigger '{trigger_name}' created successfully")
                except Error as e:
                    if "already exists" in str(e).lower():
                        logger.info(f"📁 Trigger '{trigger_name}' already exists")
                    else:
                        logger.warning(f"⚠️ Could not create trigger '{trigger_name}': {e}")
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e:
            logger.error(f"❌ Error creating triggers: {e}")
    
    def load_initial_data(self):
        """Load initial data if tables are empty"""
        try:
            full_config = DB_CONFIG.copy()
            connection = mysql.connector.connect(**full_config)
            cursor = connection.cursor()
            
            # Check if branches table is empty
            cursor.execute("SELECT COUNT(*) FROM branches")
            branch_count = cursor.fetchone()[0]
            
            if branch_count == 0:
                logger.info("Loading initial branch data...")
                
                # Insert sample branches
                branch_data = [
                    ('BR001', 'Main Branch', '123 Bank Street', 'Mumbai', 'Maharashtra', '400001', '022-12345678', 'main@bankmail.com', 'John Manager'),
                    ('BR002', 'Downtown Branch', '456 Finance Road', 'Delhi', 'Delhi', '110001', '011-87654321', 'downtown@bankmail.com', 'Jane Smith'),
                    ('BR003', 'Tech Park Branch', '789 IT Boulevard', 'Bangalore', 'Karnataka', '560001', '080-11223344', 'techpark@bankmail.com', 'Tech Manager'),
                    ('BR004', 'Commercial Branch', '321 Business District', 'Chennai', 'Tamil Nadu', '600001', '044-55667788', 'commercial@bankmail.com', 'Commerce Head'),
                    ('BR005', 'Residential Branch', '654 Housing Colony', 'Pune', 'Maharashtra', '411001', '020-99887766', 'residential@bankmail.com', 'Resi Manager')
                ]
                
                cursor.executemany("""
                    INSERT INTO branches (branch_code, branch_name, address, city, state, pincode, phone, email, manager_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, branch_data)
                
                logger.info("✅ Initial branch data loaded")
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e:
            logger.error(f"❌ Error loading initial data: {e}")
    
    def initialize_database(self):
        """Complete database initialization process"""
        logger.info("🚀 Starting database initialization...")
        
        try:
            # Step 1: Check and create database
            if not self.check_and_create_database():
                return False
            
            # Step 2: Create missing tables
            if not self.create_missing_tables():
                return False
            
            # Step 3: Create triggers
            self.create_triggers()
            
            # Step 4: Load initial data
            self.load_initial_data()
            
            logger.info("🎉 Database initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            return False

def initialize_database():
    """Convenience function to initialize database"""
    initializer = DatabaseInitializer()
    return initializer.initialize_database()

# Function to check database connection
def test_database_connection():
    """Test database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info("✅ Database connection successful")
            connection.close()
            return True
    except Error as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Run initialization if script is executed directly
    initialize_database()
