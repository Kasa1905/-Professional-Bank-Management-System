from models.database import db
from datetime import datetime, date
import logging

class Loan:
    """Loan model for handling loan-related operations"""
    
    def __init__(self):
        self.db = db
    
    def create_loan(self, loan_data):
        """
        Create a new loan application
        Args:
            loan_data (dict): Loan information
        Returns:
            int: Loan ID if successful, None otherwise
        """
        try:
            # Generate loan number if not provided
            if 'loan_number' not in loan_data:
                loan_data['loan_number'] = self.generate_loan_number()
            
            # Calculate EMI if not provided
            if 'emi_amount' not in loan_data:
                loan_data['emi_amount'] = self.calculate_emi(
                    loan_data['principal_amount'],
                    loan_data['interest_rate'],
                    loan_data['tenure_months']
                )
            
            # Set outstanding amount equal to principal initially
            loan_data['outstanding_amount'] = loan_data['principal_amount']
            
            query = """
            INSERT INTO loans (
                loan_number, customer_id, loan_type, principal_amount,
                interest_rate, tenure_months, emi_amount, outstanding_amount,
                application_date, branch_id
            ) VALUES (
                %(loan_number)s, %(customer_id)s, %(loan_type)s, %(principal_amount)s,
                %(interest_rate)s, %(tenure_months)s, %(emi_amount)s, %(outstanding_amount)s,
                %(application_date)s, %(branch_id)s
            )
            """
            
            self.db.execute_query(query, loan_data, fetch=False)
            
            # Get the last inserted loan ID
            loan_id_query = "SELECT LAST_INSERT_ID() as loan_id"
            result = self.db.execute_query(loan_id_query)
            
            if result:
                return result[0]['loan_id']
            return None
            
        except Exception as e:
            logging.error(f"Error creating loan: {e}")
            return None
    
    def generate_loan_number(self):
        """Generate unique loan number"""
        try:
            # Get loan count
            count_query = "SELECT COUNT(*) + 1 as loan_count FROM loans"
            count_result = self.db.execute_query(count_query)
            loan_count = count_result[0]['loan_count']
            
            # Generate loan number: LOAN + 6-digit number
            loan_number = f"LOAN{loan_count:06d}"
            
            return loan_number
            
        except Exception as e:
            logging.error(f"Error generating loan number: {e}")
            return None
    
    def calculate_emi(self, principal, annual_rate, tenure_months):
        """
        Calculate EMI using the formula:
        EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        Where P = Principal, r = monthly interest rate, n = tenure in months
        """
        try:
            if annual_rate == 0:
                return principal / tenure_months
            
            monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly decimal
            
            emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
                  ((1 + monthly_rate) ** tenure_months - 1)
            
            return round(emi, 2)
            
        except Exception as e:
            logging.error(f"Error calculating EMI: {e}")
            return 0
    
    def approve_loan(self, loan_id, approved_by, approval_date=None):
        """Approve a loan application"""
        try:
            if not approval_date:
                approval_date = date.today()
            
            query = """
            UPDATE loans 
            SET status = 'APPROVED', approval_date = %s, approved_by = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE loan_id = %s AND status = 'APPLIED'
            """
            
            rows_affected = self.db.execute_query(
                query, (approval_date, approved_by, loan_id), fetch=False
            )
            
            return rows_affected > 0
            
        except Exception as e:
            logging.error(f"Error approving loan: {e}")
            return False
    
    def reject_loan(self, loan_id, reason="Does not meet criteria"):
        """Reject a loan application"""
        try:
            query = """
            UPDATE loans 
            SET status = 'REJECTED', updated_at = CURRENT_TIMESTAMP
            WHERE loan_id = %s AND status = 'APPLIED'
            """
            
            rows_affected = self.db.execute_query(query, (loan_id,), fetch=False)
            return rows_affected > 0
            
        except Exception as e:
            logging.error(f"Error rejecting loan: {e}")
            return False
    
    def disburse_loan(self, loan_id, account_id, disbursement_date=None):
        """Disburse an approved loan"""
        try:
            if not disbursement_date:
                disbursement_date = date.today()
            
            # Get loan details
            loan = self.get_loan_by_id(loan_id)
            if not loan or loan['status'] != 'APPROVED':
                return False, "Loan not found or not approved"
            
            # Update loan status
            query = """
            UPDATE loans 
            SET status = 'DISBURSED', disbursement_date = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE loan_id = %s
            """
            
            rows_affected = self.db.execute_query(
                query, (disbursement_date, loan_id), fetch=False
            )
            
            if rows_affected > 0:
                # Credit the loan amount to customer's account
                from models.transaction import Transaction
                transaction_model = Transaction()
                
                success, message, new_balance = transaction_model.deposit(
                    account_id,
                    loan['principal_amount'],
                    f"Loan disbursement - {loan['loan_number']}",
                    loan['approved_by']
                )
                
                if success:
                    return True, f"Loan disbursed successfully. Amount ₹{loan['principal_amount']} credited to account."
                else:
                    # Rollback loan status
                    rollback_query = """
                    UPDATE loans 
                    SET status = 'APPROVED', disbursement_date = NULL
                    WHERE loan_id = %s
                    """
                    self.db.execute_query(rollback_query, (loan_id,), fetch=False)
                    return False, f"Failed to credit amount: {message}"
            else:
                return False, "Failed to update loan status"
                
        except Exception as e:
            logging.error(f"Error disbursing loan: {e}")
            return False, f"Error disbursing loan: {str(e)}"
    
    def get_loan_by_id(self, loan_id):
        """Get loan by ID"""
        query = """
        SELECT 
            l.*, 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, c.email,
            CONCAT(s.first_name, ' ', s.last_name) as approved_by_name,
            b.branch_name
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        LEFT JOIN staff s ON l.approved_by = s.staff_id
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE l.loan_id = %s
        """
        result = self.db.execute_query(query, (loan_id,))
        return result[0] if result else None
    
    def get_loan_by_number(self, loan_number):
        """Get loan by loan number"""
        query = """
        SELECT 
            l.*, 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, c.email,
            CONCAT(s.first_name, ' ', s.last_name) as approved_by_name,
            b.branch_name
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        LEFT JOIN staff s ON l.approved_by = s.staff_id
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE l.loan_number = %s
        """
        result = self.db.execute_query(query, (loan_number,))
        return result[0] if result else None
    
    def get_customer_loans(self, customer_id):
        """Get all loans for a customer"""
        query = """
        SELECT 
            loan_id, loan_number, loan_type, principal_amount,
            interest_rate, tenure_months, emi_amount,
            outstanding_amount, status, application_date,
            approval_date, disbursement_date
        FROM loans
        WHERE customer_id = %s
        ORDER BY application_date DESC
        """
        return self.db.execute_query(query, (customer_id,))
    
    def search_loans(self, search_term):
        """Search loans by loan number or customer name"""
        query = """
        SELECT 
            l.loan_id, l.loan_number, l.loan_type, l.principal_amount,
            l.outstanding_amount, l.status, l.application_date,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, b.branch_name
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE 
            l.loan_number LIKE %s OR
            c.first_name LIKE %s OR
            c.last_name LIKE %s OR
            c.phone LIKE %s
        ORDER BY l.application_date DESC
        """
        search_pattern = f"%{search_term}%"
        return self.db.execute_query(query, (search_pattern,) * 4)
    
    def get_pending_loans(self, branch_id=None):
        """Get all pending loan applications"""
        query = """
        SELECT 
            l.loan_id, l.loan_number, l.loan_type, l.principal_amount,
            l.application_date, l.tenure_months,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, c.annual_income, b.branch_name
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE l.status = 'APPLIED'
        """
        params = []
        
        if branch_id:
            query += " AND l.branch_id = %s"
            params.append(branch_id)
        
        query += " ORDER BY l.application_date ASC"
        
        return self.db.execute_query(query, params)
    
    def make_payment(self, loan_id, payment_amount, payment_date=None):
        """Process a loan payment"""
        try:
            if not payment_date:
                payment_date = date.today()
            
            loan = self.get_loan_by_id(loan_id)
            if not loan or loan['status'] != 'DISBURSED':
                return False, "Loan not found or not disbursed"
            
            if payment_amount <= 0:
                return False, "Payment amount must be positive"
            
            if payment_amount > loan['outstanding_amount']:
                return False, "Payment amount exceeds outstanding amount"
            
            new_outstanding = loan['outstanding_amount'] - payment_amount
            
            # Update outstanding amount
            query = """
            UPDATE loans 
            SET outstanding_amount = %s, updated_at = CURRENT_TIMESTAMP
            WHERE loan_id = %s
            """
            
            rows_affected = self.db.execute_query(
                query, (new_outstanding, loan_id), fetch=False
            )
            
            if rows_affected > 0:
                # If loan is fully paid, mark as closed
                if new_outstanding == 0:
                    close_query = """
                    UPDATE loans 
                    SET status = 'CLOSED', updated_at = CURRENT_TIMESTAMP
                    WHERE loan_id = %s
                    """
                    self.db.execute_query(close_query, (loan_id,), fetch=False)
                    return True, f"Loan payment successful. Loan is now fully paid and closed."
                else:
                    return True, f"Payment successful. Outstanding amount: ₹{new_outstanding}"
            else:
                return False, "Failed to update loan payment"
                
        except Exception as e:
            logging.error(f"Error processing loan payment: {e}")
            return False, f"Error processing payment: {str(e)}"
    
    def get_loan_summary(self, branch_id=None):
        """Get loan portfolio summary"""
        query = """
        SELECT 
            loan_type,
            COUNT(*) as total_loans,
            SUM(CASE WHEN status = 'APPLIED' THEN 1 ELSE 0 END) as pending_loans,
            SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) as approved_loans,
            SUM(CASE WHEN status = 'DISBURSED' THEN 1 ELSE 0 END) as disbursed_loans,
            SUM(CASE WHEN status = 'CLOSED' THEN 1 ELSE 0 END) as closed_loans,
            SUM(principal_amount) as total_principal,
            SUM(outstanding_amount) as total_outstanding
        FROM loans
        """
        params = []
        
        if branch_id:
            query += " WHERE branch_id = %s"
            params.append(branch_id)
        
        query += " GROUP BY loan_type ORDER BY total_principal DESC"
        
        return self.db.execute_query(query, params)
    
    def validate_loan_data(self, loan_data):
        """Validate loan data before creation"""
        errors = []
        
        # Required fields
        required_fields = ['customer_id', 'loan_type', 'principal_amount', 
                          'interest_rate', 'tenure_months', 'branch_id']
        for field in required_fields:
            if not loan_data.get(field):
                errors.append(f"{field} is required")
        
        # Loan type validation
        valid_types = ['PERSONAL', 'HOME', 'CAR', 'EDUCATION', 'BUSINESS']
        if loan_data.get('loan_type') not in valid_types:
            errors.append(f"Loan type must be one of: {', '.join(valid_types)}")
        
        # Amount validation
        principal_amount = loan_data.get('principal_amount', 0)
        if principal_amount <= 0:
            errors.append("Principal amount must be positive")
        elif principal_amount > 10000000:  # 1 crore limit
            errors.append("Principal amount cannot exceed ₹1,00,00,000")
        
        # Interest rate validation
        interest_rate = loan_data.get('interest_rate', 0)
        if interest_rate < 0 or interest_rate > 30:
            errors.append("Interest rate must be between 0% and 30%")
        
        # Tenure validation
        tenure_months = loan_data.get('tenure_months', 0)
        if tenure_months < 1 or tenure_months > 360:  # 30 years max
            errors.append("Tenure must be between 1 and 360 months")
        
        return errors
    
    def get_all_loans(self, limit=100, offset=0):
        """Get all loans with pagination"""
        query = """
        SELECT 
            l.loan_id, l.loan_number, l.loan_type, l.principal_amount,
            l.outstanding_amount, l.status, l.application_date,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.phone, b.branch_name
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN branches b ON l.branch_id = b.branch_id
        ORDER BY l.application_date DESC
        LIMIT %s OFFSET %s
        """
        return self.db.execute_query(query, (limit, offset))
