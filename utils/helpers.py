"""
Helper utilities for Bank Management System
"""

import random
import string
from datetime import datetime, date, timedelta
from typing import Union, Optional
import hashlib

def generate_customer_number() -> str:
    """Generate unique customer number"""
    timestamp = int(datetime.now().timestamp())
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return f"CUST{timestamp}{random_suffix}"

def generate_account_number(branch_code: str) -> str:
    """Generate account number for a branch"""
    timestamp = int(datetime.now().timestamp())
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{branch_code}{timestamp}{random_suffix}"

def generate_transaction_number() -> str:
    """Generate unique transaction number"""
    timestamp = int(datetime.now().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TXN{timestamp}{random_suffix}"

def generate_loan_number() -> str:
    """Generate unique loan number"""
    timestamp = int(datetime.now().timestamp())
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return f"LOAN{timestamp}{random_suffix}"

def format_currency(amount: Union[int, float], currency_symbol: str = "₹") -> str:
    """Format amount as currency string"""
    if amount is None:
        return f"{currency_symbol}0.00"
    
    return f"{currency_symbol}{amount:,.2f}"

def format_phone(phone: str) -> str:
    """Format phone number for display"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('0'):
        return f"0{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        return phone

def format_account_number(account_number: str) -> str:
    """Format account number for display"""
    if not account_number:
        return ""
    
    # Add spaces every 4 characters for readability
    formatted = ""
    for i, char in enumerate(account_number):
        if i > 0 and i % 4 == 0:
            formatted += " "
        formatted += char
    
    return formatted

def calculate_age(birth_date: Union[date, datetime]) -> int:
    """Calculate age from birth date"""
    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate EMI (Equated Monthly Installment)
    Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    """
    if annual_rate == 0:
        return principal / tenure_months
    
    monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly decimal
    
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)
    
    return round(emi, 2)

def calculate_compound_interest(principal: float, annual_rate: float, years: float, 
                              compound_frequency: int = 4) -> float:
    """
    Calculate compound interest
    A = P(1 + r/n)^(nt)
    """
    amount = principal * (1 + annual_rate / (100 * compound_frequency)) ** (compound_frequency * years)
    return round(amount - principal, 2)

def calculate_simple_interest(principal: float, annual_rate: float, years: float) -> float:
    """Calculate simple interest"""
    interest = (principal * annual_rate * years) / 100
    return round(interest, 2)

def get_financial_year(date_obj: Optional[date] = None) -> str:
    """Get financial year string (Apr-Mar)"""
    if date_obj is None:
        date_obj = date.today()
    
    if date_obj.month >= 4:  # April onwards
        start_year = date_obj.year
        end_year = date_obj.year + 1
    else:  # Jan-Mar
        start_year = date_obj.year - 1
        end_year = date_obj.year
    
    return f"FY {start_year}-{str(end_year)[2:]}"

def get_quarter(date_obj: Optional[date] = None) -> str:
    """Get quarter string"""
    if date_obj is None:
        date_obj = date.today()
    
    quarter = (date_obj.month - 1) // 3 + 1
    return f"Q{quarter} {date_obj.year}"

def days_between_dates(start_date: date, end_date: date) -> int:
    """Calculate days between two dates"""
    return (end_date - start_date).days

def add_business_days(start_date: date, business_days: int) -> date:
    """Add business days to a date (excluding weekends)"""
    current_date = start_date
    days_added = 0
    
    while days_added < business_days:
        current_date += timedelta(days=1)
        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5:  # Monday to Friday
            days_added += 1
    
    return current_date

def is_business_day(date_obj: date) -> bool:
    """Check if a date is a business day (Monday-Friday)"""
    return date_obj.weekday() < 5

def hash_sensitive_data(data: str, salt: str = "bank_salt") -> str:
    """Hash sensitive data using SHA-256"""
    return hashlib.sha256((data + salt).encode()).hexdigest()

def mask_sensitive_info(data: str, visible_chars: int = 4, mask_char: str = "*") -> str:
    """Mask sensitive information showing only last few characters"""
    if len(data) <= visible_chars:
        return mask_char * len(data)
    
    masked_length = len(data) - visible_chars
    return mask_char * masked_length + data[-visible_chars:]

def format_date(date_obj: Union[date, datetime], format_str: str = "%Y-%m-%d") -> str:
    """Format date for display"""
    if date_obj is None:
        return ""
    
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format_str)
    elif isinstance(date_obj, date):
        return date_obj.strftime(format_str)
    else:
        return str(date_obj)

def format_datetime(datetime_obj: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime for display"""
    if datetime_obj is None:
        return ""
    
    return datetime_obj.strftime(format_str)

def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[date]:
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_str, format_str).date()
    except (ValueError, TypeError):
        return None

def parse_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse datetime string to datetime object"""
    try:
        return datetime.strptime(datetime_str, format_str)
    except (ValueError, TypeError):
        return None

def get_month_start_end(year: int, month: int) -> tuple[date, date]:
    """Get start and end dates of a month"""
    start_date = date(year, month, 1)
    
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    return start_date, end_date

def get_year_start_end(year: int) -> tuple[date, date]:
    """Get start and end dates of a year"""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    return start_date, end_date

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division that handles division by zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def percentage(part: float, whole: float, decimal_places: int = 2) -> float:
    """Calculate percentage"""
    if whole == 0:
        return 0.0
    
    return round((part / whole) * 100, decimal_places)

def round_to_nearest(value: float, nearest: float = 0.01) -> float:
    """Round to nearest specified value"""
    return round(value / nearest) * nearest

def generate_random_string(length: int = 8, use_uppercase: bool = True, 
                          use_lowercase: bool = True, use_digits: bool = True) -> str:
    """Generate random string"""
    characters = ""
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    
    if not characters:
        characters = string.ascii_letters + string.digits
    
    return ''.join(random.choices(characters, k=length))

def clean_string(text: str) -> str:
    """Clean string by removing extra whitespace and special characters"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def is_valid_numeric_string(text: str) -> bool:
    """Check if string represents a valid number"""
    try:
        float(text)
        return True
    except (ValueError, TypeError):
        return False
