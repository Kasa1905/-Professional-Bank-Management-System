"""
Transaction Model for Bank Management System
Handles all transaction-related database operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)

class Transaction:
    """Transaction model for handling transaction-related operations"""
    
    def __init__(self):
        self.connection = None
    
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
    
    def generate_transaction_reference(self):
        """Generate unique transaction reference (max 20 chars)"""
        import time
        # Use milliseconds timestamp (10 digits) + 4 random chars = 14 chars max
        timestamp = int(time.time() * 1000) % 10000000000  # Keep last 10 digits
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        reference = f"T{timestamp}{random_suffix}"
        
        # Ensure uniqueness by checking database
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Keep generating until we get a unique reference
            attempts = 0
            while attempts < 5:  # Reduced attempts since collision is very unlikely
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE transaction_number = %s", (reference,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.close()
                    return reference
                
                # Generate a new reference if collision detected
                attempts += 1
                time.sleep(0.001)  # Small delay to ensure different timestamp
                timestamp = int(time.time() * 1000) % 10000000000
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                reference = f"T{timestamp}{random_suffix}"
            
            cursor.close()
            # Fallback to simple timestamp + random if still colliding
            return f"T{int(time.time()) % 1000000}{random.randint(1000, 9999)}"
            
        except Exception as e:
            logger.error(f"Error generating unique reference: {e}")
            # Fallback to timestamp + random number (fits in 20 chars)
            return f"T{int(time.time()) % 1000000}{random.randint(1000, 9999)}"
    
    def get_accounts_for_dropdown(self):
        """Get all active accounts for dropdown selection"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    a.account_id,
                    a.account_number,
                    a.account_type,
                    a.balance,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name
                FROM accounts a
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE a.status = 'ACTIVE'
                ORDER BY a.account_number
            """
            
            cursor.execute(query)
            accounts = cursor.fetchall()
            cursor.close()
            
            return accounts
            
        except Error as e:
            logger.error(f"Error fetching accounts for dropdown: {e}")
            return []
    
    def get_account_balance(self, account_id):
        """Get current balance for an account"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT balance FROM accounts WHERE account_id = %s"
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return float(result[0]) if result else 0.0
            
        except Error as e:
            logger.error(f"Error getting account balance: {e}")
            return 0.0
    
    def deposit(self, account_id, amount, description="Deposit", reference=None):
        """Process a deposit transaction"""
        try:
            if reference is None:
                reference = self.generate_transaction_reference()
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Start transaction
            connection.start_transaction()
            
            # Get current balance
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s FOR UPDATE", (account_id,))
            result = cursor.fetchone()
            if not result:
                connection.rollback()
                return {"success": False, "message": "Account not found"}
            
            current_balance = float(result[0])
            new_balance = current_balance + amount
            
            # Update account balance
            cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_id = %s",
                (new_balance, account_id)
            )
            
            # Insert transaction record
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_number, account_id, transaction_type, amount, 
                    balance_before, balance_after, description, transaction_date, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                reference, account_id, 'DEPOSIT', amount, 
                current_balance, new_balance, description, datetime.now(), 'COMPLETED'
            ))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Deposit successful - Account: {account_id}, Amount: {amount}, New Balance: {new_balance}")
            return {
                "success": True, 
                "message": "Deposit successful",
                "new_balance": new_balance,
                "reference": reference
            }
            
        except Error as e:
            connection.rollback()
            logger.error(f"Deposit error: {e}")
            return {"success": False, "message": f"Deposit failed: {str(e)}"}
    
    def withdraw(self, account_id, amount, description="Withdrawal", reference=None):
        """Process a withdrawal transaction"""
        try:
            if reference is None:
                reference = self.generate_transaction_reference()
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Start transaction
            connection.start_transaction()
            
            # Get current balance
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s FOR UPDATE", (account_id,))
            result = cursor.fetchone()
            if not result:
                connection.rollback()
                return {"success": False, "message": "Account not found"}
            
            current_balance = float(result[0])
            
            # Check sufficient balance
            if current_balance < amount:
                connection.rollback()
                return {"success": False, "message": "Insufficient balance"}
            
            new_balance = current_balance - amount
            
            # Update account balance
            cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_id = %s",
                (new_balance, account_id)
            )
            
            # Insert transaction record
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_number, account_id, transaction_type, amount, 
                    balance_before, balance_after, description, transaction_date, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                reference, account_id, 'WITHDRAWAL', amount, 
                current_balance, new_balance, description, datetime.now(), 'COMPLETED'
            ))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Withdrawal successful - Account: {account_id}, Amount: {amount}, New Balance: {new_balance}")
            return {
                "success": True, 
                "message": "Withdrawal successful",
                "new_balance": new_balance,
                "reference": reference
            }
            
        except Error as e:
            connection.rollback()
            logger.error(f"Withdrawal error: {e}")
            return {"success": False, "message": f"Withdrawal failed: {str(e)}"}
    
    def transfer(self, from_account_id, to_account_id, amount, description="Transfer", reference=None):
        """Process a transfer between accounts"""
        try:
            if reference is None:
                reference = self.generate_transaction_reference()
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Start transaction
            connection.start_transaction()
            
            # Get both account balances with locks
            cursor.execute("""
                SELECT balance FROM accounts 
                WHERE account_id IN (%s, %s) 
                ORDER BY account_id FOR UPDATE
            """, (from_account_id, to_account_id))
            
            results = cursor.fetchall()
            if len(results) != 2:
                connection.rollback()
                return {"success": False, "message": "One or both accounts not found"}
            
            # Get current balances
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
            from_balance = float(cursor.fetchone()[0])
            
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (to_account_id,))
            to_balance = float(cursor.fetchone()[0])
            
            # Check sufficient balance in from_account
            if from_balance < amount:
                connection.rollback()
                return {"success": False, "message": "Insufficient balance in source account"}
            
            new_from_balance = from_balance - amount
            new_to_balance = to_balance + amount
            
            # Update both account balances
            cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_id = %s",
                (new_from_balance, from_account_id)
            )
            cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_id = %s",
                (new_to_balance, to_account_id)
            )
            
            # Insert transaction records for both accounts
            # Insert transaction records for both accounts with unique transaction numbers
            transaction_time = datetime.now()
            
            # Generate unique references for each leg of the transfer
            debit_reference = f"{reference}O"  # O for Out (shorter suffix)
            credit_reference = f"{reference}I"  # I for In (shorter suffix)
            
            # Debit transaction for from_account
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_number, account_id, transaction_type, amount, 
                    balance_before, balance_after, description, transaction_date, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                debit_reference, from_account_id, 'TRANSFER_OUT', amount, 
                from_balance, new_from_balance, f"{description} - To Account", transaction_time, 'COMPLETED'
            ))
            
            # Credit transaction for to_account
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_number, account_id, transaction_type, amount, 
                    balance_before, balance_after, description, transaction_date, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                credit_reference, to_account_id, 'TRANSFER_IN', amount, 
                to_balance, new_to_balance, f"{description} - From Account", transaction_time, 'COMPLETED'
            ))
            
            connection.commit()
            cursor.close()
            
            logger.info(f"Transfer successful - From: {from_account_id} To: {to_account_id}, Amount: {amount}")
            return {
                "success": True, 
                "message": "Transfer successful",
                "from_balance": new_from_balance,
                "to_balance": new_to_balance,
                "reference": reference
            }
            
        except Error as e:
            connection.rollback()
            logger.error(f"Transfer error: {e}")
            return {"success": False, "message": f"Transfer failed: {str(e)}"}
    
    def get_all_transactions(self, limit=1000):
        """Get all transactions with account and customer information"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    t.transaction_id,
                    t.account_id,
                    a.account_number,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    t.transaction_type,
                    t.amount,
                    t.balance_after,
                    t.description,
                    t.transaction_number,
                    t.transaction_date
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                ORDER BY t.transaction_date DESC
                LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            transactions = cursor.fetchall()
            cursor.close()
            
            return transactions
            
        except Error as e:
            logger.error(f"Error fetching transactions: {e}")
            return []
    
    def search_transactions(self, search_term, limit=1000):
        """Search transactions by various criteria"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            search_pattern = f"%{search_term}%"
            
            query = """
                SELECT 
                    t.transaction_id,
                    t.account_id,
                    a.account_number,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    t.transaction_type,
                    t.amount,
                    t.balance_after,
                    t.description,
                    t.transaction_number,
                    t.transaction_date
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE 
                    a.account_number LIKE %s OR
                    CONCAT(c.first_name, ' ', c.last_name) LIKE %s OR
                    t.transaction_type LIKE %s OR
                    t.description LIKE %s OR
                    t.transaction_number LIKE %s
                ORDER BY t.transaction_date DESC
                LIMIT %s
            """
            
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                                 search_pattern, search_pattern, limit))
            transactions = cursor.fetchall()
            cursor.close()
            
            return transactions
            
        except Error as e:
            logger.error(f"Error searching transactions: {e}")
            return []
    
    def get_account_transactions(self, account_id, limit=100):
        """Get transactions for a specific account"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.balance_after,
                    t.description,
                    t.transaction_number,
                    t.transaction_date
                FROM transactions t
                WHERE t.account_id = %s
                ORDER BY t.transaction_date DESC
                LIMIT %s
            """
            
            cursor.execute(query, (account_id, limit))
            transactions = cursor.fetchall()
            cursor.close()
            
            return transactions
            
        except Error as e:
            logger.error(f"Error fetching account transactions: {e}")
            return []
    
    def get_transactions_by_date_range(self, start_date, end_date, account_id=None):
        """Get transactions within a date range"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            base_query = """
                SELECT 
                    t.transaction_id,
                    t.account_id,
                    a.account_number,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    t.transaction_type,
                    t.amount,
                    t.balance_after,
                    t.description,
                    t.transaction_number,
                    t.transaction_date
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE DATE(t.transaction_date) BETWEEN %s AND %s
            """
            
            params = [start_date, end_date]
            
            if account_id:
                base_query += " AND t.account_id = %s"
                params.append(account_id)
            
            base_query += " ORDER BY t.transaction_date DESC"
            
            cursor.execute(base_query, params)
            transactions = cursor.fetchall()
            cursor.close()
            
            return transactions
            
        except Error as e:
            logger.error(f"Error fetching transactions by date range: {e}")
            return []
    
    def get_transaction_summary(self, account_id=None, days=30):
        """Get transaction summary for the last N days"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            base_query = """
                SELECT 
                    transaction_type,
                    COUNT(*) as count,
                    SUM(amount) as total_amount
                FROM transactions t
                WHERE DATE(t.transaction_date) >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            """
            
            params = [days]
            
            if account_id:
                base_query += " AND t.account_id = %s"
                params.append(account_id)
            
            base_query += " GROUP BY transaction_type"
            
            cursor.execute(base_query, params)
            summary = cursor.fetchall()
            cursor.close()
            
            return summary
            
        except Error as e:
            logger.error(f"Error getting transaction summary: {e}")
            return []
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection()
