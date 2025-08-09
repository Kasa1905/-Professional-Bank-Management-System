"""
Account Model for Bank Management System
Handles all account-related database operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime
import logging
import random
import string

# Set up logger
logger = logging.getLogger(__name__)
import random
import string

logger = logging.getLogger(__name__)

class Account:
    """Account model for handling account-related operations"""
    
    def __init__(self):
        self.connection = None
        # Account type mapping: GUI values -> Database ENUM values
        self.account_type_mapping = {
            'SAVINGS': 'SAVINGS',
            'CURRENT': 'CURRENT', 
            'FIXED_DEPOSIT': 'FD',
            'SALARY': 'SALARY',  # Now map SALARY to SALARY
            'FD': 'FD',
            'RD': 'RD'
        }
        
        # Reverse mapping for display: Database -> Display
        self.display_type_mapping = {
            'SAVINGS': 'SAVINGS',
            'CURRENT': 'CURRENT',
            'FD': 'FIXED_DEPOSIT',
            'RD': 'RECURRING_DEPOSIT',
            'SALARY': 'SALARY'
        }
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def generate_account_number(self):
        """Generate unique account number"""
        timestamp = str(int(datetime.now().timestamp()))[-8:]  # Last 8 digits of timestamp
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"{timestamp}{random_suffix}"
    
    def get_all_accounts(self):
        """Get all accounts with customer information"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                a.account_id,
                a.account_number,
                a.account_type,
                a.balance,
                a.status,
                a.opening_date,
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                c.phone
            FROM accounts a
            LEFT JOIN customers c ON a.customer_id = c.customer_id
            ORDER BY a.created_date DESC
            """
            
            cursor.execute(query)
            result = cursor.fetchall()
            
            # Map database account types to display types
            for account in result:
                db_type = account['account_type']
                account['account_type_display'] = self.display_type_mapping.get(db_type, db_type)
                
            return result
            
        except mysql.connector.Error as e:
            print(f"Error fetching accounts: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_customers_for_dropdown(self):
        """Get active customers for account creation dropdown"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT customer_id, customer_number, first_name, last_name
            FROM customers 
            WHERE status = 'ACTIVE'
            ORDER BY first_name, last_name
            """
            
            cursor.execute(query)
            customers = cursor.fetchall()
            cursor.close()
            return customers
            
        except Error as e:
            logger.error(f"Error fetching customers: {e}")
            return []
    
    def get_branches_for_dropdown(self):
        """Get branches for dropdown (simplified - return empty for now)"""
        # Since we don't have branches table, return empty list
        # In a real system, you might have a branches table
        return []
    
    def create_account(self, account_data):
        """
        Create a new account
        Args:
            account_data (dict): Account information
        Returns:
            str: Account number if successful, None otherwise
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Generate account number if not provided
            if 'account_number' not in account_data:
                account_data['account_number'] = self.generate_account_number()
            
            # Map account type from GUI to database enum value
            gui_account_type = account_data['account_type']
            db_account_type = self.account_type_mapping.get(gui_account_type, gui_account_type)
            
            # Prepare the SQL query (removed branch_id)
            query = """
            INSERT INTO accounts (
                account_number, customer_id, account_type, balance, 
                status, created_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
            """
            
            # Prepare the data tuple (removed branch_id) with mapped account type
            data = (
                account_data['account_number'],
                account_data['customer_id'],
                db_account_type,  # Use mapped account type
                account_data.get('initial_balance', 0.0),
                'ACTIVE',
                datetime.now()
            )
            
            cursor.execute(query, data)
            connection.commit()
            
            account_id = cursor.lastrowid
            logger.info(f"Account created successfully with ID: {account_id}")
            
            cursor.close()
            return account_data['account_number']
            
        except Error as e:
            logger.error(f"Error creating account: {e}")
            if connection:
                connection.rollback()
            raise
    
    def get_account_by_id(self, account_id):
        """Get account details by ID"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                a.*, 
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                c.phone
            FROM accounts a
            LEFT JOIN customers c ON a.customer_id = c.customer_id
            WHERE a.account_id = %s
            """
            
            cursor.execute(query, (account_id,))
            account = cursor.fetchone()
            cursor.close()
            return account
            
        except Error as e:
            logger.error(f"Error fetching account: {e}")
            return None
    
    def update_account_status(self, account_id, status):
        """Update account status (ACTIVE/INACTIVE/CLOSED)"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Also update closing_date when status is CLOSED
            if status == 'CLOSED':
                query = """
                UPDATE accounts 
                SET status = %s, closing_date = %s, updated_date = %s 
                WHERE account_id = %s
                """
                cursor.execute(query, (status, datetime.now().date(), datetime.now(), account_id))
            else:
                query = "UPDATE accounts SET status = %s, updated_date = %s WHERE account_id = %s"
                cursor.execute(query, (status, datetime.now(), account_id))
            
            connection.commit()
            
            success = cursor.rowcount > 0
            cursor.close()
            
            if success:
                logger.info(f"Account {account_id} status updated to {status}")
                print(f"Account {account_id} status updated to {status}")  # Debug print
            else:
                print(f"No rows affected when updating account {account_id}")  # Debug print
            
            return success
            
        except mysql.connector.Error as e:
            logger.error(f"Error updating account status: {e}")
            print(f"Database error updating account status: {e}")  # Debug print
            if connection:
                connection.rollback()
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating account status: {e}")
            print(f"Unexpected error updating account status: {e}")  # Debug print
            if connection:
                connection.rollback()
            return False
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def get_account_balance(self, account_id):
        """Get current account balance"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT balance FROM accounts WHERE account_id = %s"
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else 0.0
            
        except Error as e:
            logger.error(f"Error fetching account balance: {e}")
            return 0.0
    
    def search_accounts(self, search_term):
        """Search accounts by account number, customer name, or phone"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                a.account_id, a.account_number, a.account_type, a.balance, 
                a.status, a.created_date,
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                c.phone
            FROM accounts a
            LEFT JOIN customers c ON a.customer_id = c.customer_id
            WHERE a.account_number LIKE %s 
               OR c.first_name LIKE %s 
               OR c.last_name LIKE %s
               OR c.phone LIKE %s
               OR CONCAT(c.first_name, ' ', c.last_name) LIKE %s
            ORDER BY a.created_date DESC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                                 search_pattern, search_pattern))
            accounts = cursor.fetchall()
            cursor.close()
            return accounts
            
        except Error as e:
            logger.error(f"Error searching accounts: {e}")
            return []
