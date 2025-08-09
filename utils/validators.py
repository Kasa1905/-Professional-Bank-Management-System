"""
Validation utilities for Bank Management System
"""

import re
from datetime import datetime, date
from typing import List, Any, Optional

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_email(email: Optional[str]) -> bool:
    """Validate email format"""
    if not email:
        return True  # Email is optional
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format (Indian format)"""
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid Indian phone number
    if len(digits_only) == 10 and digits_only[0] in '6789':
        return True
    elif len(digits_only) == 11 and digits_only.startswith('0'):
        return True
    elif len(digits_only) == 12 and digits_only.startswith('91'):
        return True
    elif len(digits_only) == 13 and digits_only.startswith('+91'):
        return True
    
    return False

def validate_pan(pan: str) -> bool:
    """Validate PAN card format"""
    if not pan:
        return False
    
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan.upper()))

def validate_aadhar(aadhar: str) -> bool:
    """Validate Aadhar number format"""
    if not aadhar:
        return False
    
    # Remove spaces and hyphens
    aadhar_clean = re.sub(r'[\s-]', '', aadhar)
    
    # Check if it's 12 digits
    if len(aadhar_clean) != 12 or not aadhar_clean.isdigit():
        return False
    
    # Basic Verhoeff algorithm check (simplified)
    return True

def validate_pincode(pincode: str) -> bool:
    """Validate Indian pincode format"""
    if not pincode:
        return False
    
    return bool(re.match(r'^[1-9][0-9]{5}$', pincode))

def validate_amount(amount: Any) -> bool:
    """Validate monetary amount"""
    try:
        amt = float(amount)
        return amt >= 0
    except (ValueError, TypeError):
        return False

def validate_positive_number(value: Any) -> bool:
    """Validate positive number"""
    try:
        num = float(value)
        return num > 0
    except (ValueError, TypeError):
        return False

def validate_date(date_str: str, date_format: str = '%Y-%m-%d') -> bool:
    """Validate date format and value"""
    if not date_str:
        return False
    
    try:
        parsed_date = datetime.strptime(date_str, date_format).date()
        
        # Check if date is reasonable (not in future, not too old)
        today = date.today()
        min_date = date(1900, 1, 1)
        
        return min_date <= parsed_date <= today
    except ValueError:
        return False

def validate_age(birth_date: date, min_age: int = 18, max_age: int = 100) -> bool:
    """Validate age based on birth date"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    return min_age <= age <= max_age

def validate_account_number(account_number: str) -> bool:
    """Validate account number format"""
    if not account_number:
        return False
    
    # Account number should be alphanumeric and 8-20 characters
    return bool(re.match(r'^[A-Z0-9]{8,20}$', account_number.upper()))

def validate_ifsc_code(ifsc: str) -> bool:
    """Validate IFSC code format"""
    if not ifsc:
        return False
    
    pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(pattern, ifsc.upper()))

def sanitize_string(text: str, max_length: int = None) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
    """Validate that required fields are present and not empty"""
    errors = []
    
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == "":
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    return errors

def validate_customer_data(customer_data: dict) -> List[str]:
    """Comprehensive customer data validation"""
    errors = []
    
    # Required fields
    required_fields = [
        'first_name', 'last_name', 'date_of_birth', 'gender',
        'phone', 'address', 'city', 'state', 'pincode',
        'id_proof_type', 'id_proof_number'
    ]
    
    errors.extend(validate_required_fields(customer_data, required_fields))
    
    # Email validation (optional)
    if customer_data.get('email') and not validate_email(customer_data['email']):
        errors.append("Invalid email format")
    
    # Phone validation
    if customer_data.get('phone') and not validate_phone(customer_data['phone']):
        errors.append("Invalid phone number format")
    
    # Date of birth validation
    if customer_data.get('date_of_birth'):
        dob_str = customer_data['date_of_birth']
        if isinstance(dob_str, str) and not validate_date(dob_str):
            errors.append("Invalid date of birth format (use YYYY-MM-DD)")
        elif isinstance(dob_str, (date, datetime)):
            if not validate_age(dob_str if isinstance(dob_str, date) else dob_str.date()):
                errors.append("Customer must be between 18 and 100 years old")
    
    # Gender validation
    if customer_data.get('gender') and customer_data['gender'] not in ['MALE', 'FEMALE', 'OTHER']:
        errors.append("Gender must be MALE, FEMALE, or OTHER")
    
    # Pincode validation
    if customer_data.get('pincode') and not validate_pincode(customer_data['pincode']):
        errors.append("Invalid pincode format")
    
    # ID proof validation
    id_proof_type = customer_data.get('id_proof_type')
    id_proof_number = customer_data.get('id_proof_number')
    
    if id_proof_type == 'PAN' and id_proof_number and not validate_pan(id_proof_number):
        errors.append("Invalid PAN card format")
    elif id_proof_type == 'AADHAR' and id_proof_number and not validate_aadhar(id_proof_number):
        errors.append("Invalid Aadhar number format")
    
    # Annual income validation (optional)
    if customer_data.get('annual_income') and not validate_positive_number(customer_data['annual_income']):
        errors.append("Annual income must be a positive number")
    
    return errors

def validate_account_data(account_data: dict) -> List[str]:
    """Comprehensive account data validation"""
    errors = []
    
    # Required fields
    required_fields = ['customer_id', 'account_type', 'branch_id']
    errors.extend(validate_required_fields(account_data, required_fields))
    
    # Account type validation
    valid_account_types = ['SAVINGS', 'CURRENT', 'FD']
    if account_data.get('account_type') not in valid_account_types:
        errors.append(f"Account type must be one of: {', '.join(valid_account_types)}")
    
    # Balance validation
    if account_data.get('balance') is not None:
        if not validate_amount(account_data['balance']):
            errors.append("Balance must be a non-negative number")
    
    # Interest rate validation
    if account_data.get('interest_rate') is not None:
        try:
            rate = float(account_data['interest_rate'])
            if rate < 0 or rate > 30:
                errors.append("Interest rate must be between 0% and 30%")
        except (ValueError, TypeError):
            errors.append("Interest rate must be a valid number")
    
    return errors

def validate_transaction_data(transaction_data: dict) -> List[str]:
    """Comprehensive transaction data validation"""
    errors = []
    
    # Required fields
    required_fields = ['account_id', 'transaction_type', 'amount']
    errors.extend(validate_required_fields(transaction_data, required_fields))
    
    # Transaction type validation
    valid_transaction_types = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'INTEREST', 'FEE']
    if transaction_data.get('transaction_type') not in valid_transaction_types:
        errors.append(f"Transaction type must be one of: {', '.join(valid_transaction_types)}")
    
    # Amount validation
    if transaction_data.get('amount') and not validate_positive_number(transaction_data['amount']):
        errors.append("Transaction amount must be a positive number")
    
    return errors

def validate_loan_data(loan_data: dict) -> List[str]:
    """Comprehensive loan data validation"""
    errors = []
    
    # Required fields
    required_fields = ['customer_id', 'loan_type', 'principal_amount', 
                      'interest_rate', 'tenure_months']
    errors.extend(validate_required_fields(loan_data, required_fields))
    
    # Loan type validation
    valid_loan_types = ['PERSONAL', 'HOME', 'CAR', 'EDUCATION', 'BUSINESS']
    if loan_data.get('loan_type') not in valid_loan_types:
        errors.append(f"Loan type must be one of: {', '.join(valid_loan_types)}")
    
    # Principal amount validation
    if loan_data.get('principal_amount'):
        if not validate_positive_number(loan_data['principal_amount']):
            errors.append("Principal amount must be a positive number")
        elif float(loan_data['principal_amount']) > 10000000:  # 1 crore limit
            errors.append("Principal amount cannot exceed ₹1,00,00,000")
    
    # Interest rate validation
    if loan_data.get('interest_rate'):
        try:
            rate = float(loan_data['interest_rate'])
            if rate < 0 or rate > 30:
                errors.append("Interest rate must be between 0% and 30%")
        except (ValueError, TypeError):
            errors.append("Interest rate must be a valid number")
    
    # Tenure validation
    if loan_data.get('tenure_months'):
        try:
            tenure = int(loan_data['tenure_months'])
            if tenure < 1 or tenure > 360:  # 30 years max
                errors.append("Tenure must be between 1 and 360 months")
        except (ValueError, TypeError):
            errors.append("Tenure must be a valid number")
    
    return errors
