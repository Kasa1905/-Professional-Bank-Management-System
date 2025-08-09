"""
Customer Model for Bank Management System
Handles all customer-related database operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime, date
import logging
import random
import string

logger = logging.getLogger(__name__)

class Customer:
    """Customer model for handling customer-related operations"""
    
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
    
    def generate_customer_number(self):
        """Generate unique customer number"""
        timestamp = int(datetime.now().timestamp())
        random_suffix = ''.join(random.choices(string.digits, k=3))
        return f"CUST{timestamp}{random_suffix}"
    
    def create_customer(self, customer_data):
        """
        Create a new customer
        Args:
            customer_data (dict): Customer information
        Returns:
            str: Customer number if successful, None otherwise
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Generate customer number if not provided
            if 'customer_number' not in customer_data:
                customer_data['customer_number'] = self.generate_customer_number()
            
            # Prepare the SQL query
            query = """
            INSERT INTO customers (
                customer_number, first_name, last_name, date_of_birth, 
                gender, phone, email, address, city, state, pincode, 
                pan_number, aadhar_number, annual_income, occupation, 
                branch_id, status, created_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            
            # Prepare the data tuple
            data = (
                customer_data['customer_number'],
                customer_data.get('first_name', ''),
                customer_data.get('last_name', ''),
                customer_data.get('date_of_birth', '1990-01-01'),
                customer_data.get('gender', 'MALE'),
                customer_data.get('phone', ''),
                customer_data.get('email', ''),
                customer_data.get('address', ''),
                customer_data.get('city', ''),
                customer_data.get('state', ''),
                customer_data.get('pincode', ''),
                customer_data.get('pan_number', None),
                customer_data.get('aadhar_number', None),
                customer_data.get('annual_income', 0.0),
                customer_data.get('occupation', ''),
                customer_data.get('branch_id', 1),
                'ACTIVE',
                datetime.now()
            )
            
            cursor.execute(query, data)
            connection.commit()
            
            customer_id = cursor.lastrowid
            logger.info(f"Customer created successfully with ID: {customer_id}")
            
            cursor.close()
            return customer_data['customer_number']
            
        except Error as e:
            logger.error(f"Error creating customer: {e}")
            if connection:
                connection.rollback()
            raise
    
    def get_all_customers(self):
        """Get all customers with branch information"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                c.customer_id, c.customer_number, c.first_name, c.last_name,
                c.date_of_birth, c.gender, c.phone, c.email, c.address,
                c.city, c.state, c.pincode, c.pan_number, c.aadhar_number,
                c.annual_income, c.occupation, c.status, c.created_date,
                COALESCE(b.branch_name, 'Unknown') as branch_name,
                COALESCE(b.branch_code, 'N/A') as branch_code
            FROM customers c
            LEFT JOIN branches b ON c.branch_id = b.branch_id
            ORDER BY c.created_date DESC
            """
            
            cursor.execute(query)
            customers = cursor.fetchall()
            
            cursor.close()
            return customers
            
        except Error as e:
            logger.error(f"Error fetching customers: {e}")
            raise
    
    def search_customers(self, search_term):
        """Search customers by name, phone, email, or customer number"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                c.customer_id, c.customer_number, c.first_name, c.last_name,
                c.phone, c.email, c.status, c.created_date,
                COALESCE(b.branch_name, 'Unknown') as branch_name,
                COALESCE(b.branch_code, 'N/A') as branch_code
            FROM customers c
            LEFT JOIN branches b ON c.branch_id = b.branch_id
            WHERE 
                c.first_name LIKE %s OR c.last_name LIKE %s OR 
                c.phone LIKE %s OR c.email LIKE %s OR 
                c.customer_number LIKE %s
            ORDER BY c.created_date DESC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                                 search_pattern, search_pattern))
            
            customers = cursor.fetchall()
            cursor.close()
            return customers
            
        except Error as e:
            logger.error(f"Error searching customers: {e}")
            raise
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                c.*, 
                COALESCE(b.branch_name, 'Unknown') as branch_name,
                COALESCE(b.branch_code, 'N/A') as branch_code
            FROM customers c
            LEFT JOIN branches b ON c.branch_id = b.branch_id
            WHERE c.customer_id = %s
            """
            
            cursor.execute(query, (customer_id,))
            customer = cursor.fetchone()
            
            cursor.close()
            return customer
            
        except Error as e:
            logger.error(f"Error fetching customer by ID: {e}")
            raise
    
    def update_customer(self, customer_id, customer_data):
        """Update customer information"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            allowed_fields = ['first_name', 'last_name', 'phone', 'email', 'address', 
                            'city', 'state', 'pincode', 'annual_income', 'occupation', 'status']
            
            for field in allowed_fields:
                if field in customer_data:
                    update_fields.append(f"{field} = %s")
                    values.append(customer_data[field])
            
            if not update_fields:
                return False
            
            # Add updated timestamp
            update_fields.append("updated_date = %s")
            values.append(datetime.now())
            values.append(customer_id)
            
            query = f"""
            UPDATE customers 
            SET {', '.join(update_fields)}
            WHERE customer_id = %s
            """
            
            cursor.execute(query, values)
            connection.commit()
            
            success = cursor.rowcount > 0
            cursor.close()
            
            if success:
                logger.info(f"Customer {customer_id} updated successfully")
            
            return success
            
        except Error as e:
            logger.error(f"Error updating customer: {e}")
            if connection:
                connection.rollback()
            raise
    
    def delete_customer(self, customer_id):
        """Soft delete customer (set status to INACTIVE)"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            UPDATE customers 
            SET status = 'INACTIVE', updated_date = %s 
            WHERE customer_id = %s
            """
            
            cursor.execute(query, (datetime.now(), customer_id))
            connection.commit()
            
            success = cursor.rowcount > 0
            cursor.close()
            
            if success:
                logger.info(f"Customer {customer_id} deactivated successfully")
            
            return success
            
        except Error as e:
            logger.error(f"Error deactivating customer: {e}")
            if connection:
                connection.rollback()
            raise
    
    def get_customer_statistics(self):
        """Get customer statistics"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                COUNT(*) as total_customers,
                COUNT(CASE WHEN status = 'ACTIVE' THEN 1 END) as active_customers,
                COUNT(CASE WHEN status = 'INACTIVE' THEN 1 END) as inactive_customers,
                AVG(annual_income) as avg_income
            FROM customers
            """
            
            cursor.execute(query)
            stats = cursor.fetchone()
            
            cursor.close()
            return stats
            
        except Error as e:
            logger.error(f"Error fetching customer statistics: {e}")
            raise
            
            query = """
            INSERT INTO customers (
                customer_number, first_name, last_name, date_of_birth, gender, 
                phone, email, address, city, state, pincode, 
                pan_number, aadhar_number, annual_income, occupation, branch_id
            ) VALUES (
                %(customer_number)s, %(first_name)s, %(last_name)s, %(date_of_birth)s, %(gender)s,
                %(phone)s, %(email)s, %(address)s, %(city)s, %(state)s,
                %(pincode)s, %(pan_number)s, %(aadhar_number)s,
                %(annual_income)s, %(occupation)s, %(branch_id)s
            )
            """
            
            self.db.execute_query(query, customer_data, fetch=False)
            
            # Get the last inserted customer ID
            customer_id_query = "SELECT LAST_INSERT_ID() as customer_id"
            result = self.db.execute_query(customer_id_query)
            
            if result:
                return result[0]['customer_id']
            return None
            
        except Exception as e:
            logging.error(f"Error creating customer: {e}")
            return None
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        query = "SELECT * FROM customers WHERE customer_id = %s"
        result = self.db.execute_query(query, (customer_id,))
        return result[0] if result else None
    
    def get_customer_by_number(self, customer_number):
        """Get customer by customer number"""
        query = "SELECT * FROM customers WHERE customer_number = %s"
        result = self.db.execute_query(query, (customer_number,))
        return result[0] if result else None
    
    def search_customers(self, search_term):
        """
        Search customers by name, phone, or email
        Args:
            search_term (str): Search term
        Returns:
            list: List of matching customers
        """
        query = """
        SELECT 
            customer_id, customer_number,
            CONCAT(first_name, ' ', last_name) as customer_name,
            phone, email, status
        FROM customers 
        WHERE 
            first_name LIKE %s OR 
            last_name LIKE %s OR 
            phone LIKE %s OR 
            email LIKE %s OR
            customer_number LIKE %s
        ORDER BY first_name, last_name
        """
        search_pattern = f"%{search_term}%"
        return self.db.execute_query(query, (search_pattern,) * 5)
    
    def update_customer(self, customer_id, customer_data):
        """Update customer information"""
        try:
            # Build dynamic update query based on provided data
            set_clauses = []
            params = []
            
            for field, value in customer_data.items():
                if value is not None:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            query = f"""
            UPDATE customers 
            SET {', '.join(set_clauses)}, updated_date = CURRENT_TIMESTAMP
            WHERE customer_id = %s
            """
            params.append(customer_id)
            
            rows_affected = self.db.execute_query(query, params, fetch=False)
            return rows_affected > 0
            
        except Exception as e:
            logging.error(f"Error updating customer: {e}")
            return False
    
    def get_customer_accounts(self, customer_id):
        """Get all accounts for a customer"""
        query = """
        SELECT 
            a.account_id, a.account_number, a.account_type,
            a.balance, a.status, a.opening_date,
            b.branch_name
        FROM accounts a
        JOIN branches b ON a.branch_id = b.branch_id
        WHERE a.customer_id = %s
        ORDER BY a.opening_date DESC
        """
        return self.db.execute_query(query, (customer_id,))
    
    def get_customer_loans(self, customer_id):
        """Get all loans for a customer"""
        query = """
        SELECT 
            loan_id, loan_number, loan_type, principal_amount,
            interest_rate, tenure_months, emi_amount,
            outstanding_amount, status, application_date
        FROM loans
        WHERE customer_id = %s
        ORDER BY application_date DESC
        """
        return self.db.execute_query(query, (customer_id,))
    
    def get_customer_summary(self, customer_id):
        """Get customer summary with accounts and balances"""
        query = """
        SELECT 
            c.customer_id, c.customer_number,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, c.email, c.status,
            COUNT(DISTINCT a.account_id) as total_accounts,
            SUM(a.balance) as total_balance,
            COUNT(DISTINCT l.loan_id) as total_loans,
            SUM(l.outstanding_amount) as total_loan_amount
        FROM customers c
        LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'ACTIVE'
        LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.status IN ('APPROVED', 'DISBURSED')
        WHERE c.customer_id = %s
        GROUP BY c.customer_id
        """
        result = self.db.execute_query(query, (customer_id,))
        return result[0] if result else None
    
    def deactivate_customer(self, customer_id):
        """Deactivate a customer account"""
        try:
            query = """
            UPDATE customers 
            SET status = 'INACTIVE', updated_at = CURRENT_TIMESTAMP
            WHERE customer_id = %s
            """
            rows_affected = self.db.execute_query(query, (customer_id,), fetch=False)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deactivating customer: {e}")
            return False
    

    
    def validate_customer_data(self, customer_data):
        """Validate customer data before insertion/update"""
        errors = []
        
        # Required fields validation
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 
                          'phone', 'address', 'city', 'state', 'pincode', 
                          'id_proof_type', 'id_proof_number']
        
        for field in required_fields:
            if not customer_data.get(field):
                errors.append(f"{field} is required")
        
        # Email validation (if provided)
        if customer_data.get('email'):
            email = customer_data['email']
            if '@' not in email or '.' not in email:
                errors.append("Invalid email format")
        
        # Phone validation
        phone = customer_data.get('phone', '')
        if len(phone) < 10:
            errors.append("Phone number must be at least 10 digits")
        
        # Date of birth validation
        if customer_data.get('date_of_birth'):
            try:
                dob = customer_data['date_of_birth']
                if isinstance(dob, str):
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                if age < 18:
                    errors.append("Customer must be at least 18 years old")
                elif age > 100:
                    errors.append("Invalid date of birth")
                    
            except ValueError:
                errors.append("Invalid date format. Use YYYY-MM-DD")
        
        return errors
