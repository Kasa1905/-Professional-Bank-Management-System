"""
Constants and enumerations for Bank Management System
"""

from enum import Enum

class AccountType(Enum):
    """Account types"""
    SAVINGS = "Savings"
    CURRENT = "Current"
    FIXED_DEPOSIT = "Fixed Deposit"
    RECURRING_DEPOSIT = "Recurring Deposit"

class TransactionType(Enum):
    """Transaction types"""
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"
    INTEREST_CREDIT = "Interest Credit"
    CHARGES = "Charges"
    LOAN_DISBURSEMENT = "Loan Disbursement"
    LOAN_PAYMENT = "Loan Payment"

class LoanType(Enum):
    """Loan types"""
    PERSONAL = "Personal Loan"
    HOME = "Home Loan"
    CAR = "Car Loan"
    EDUCATION = "Education Loan"
    BUSINESS = "Business Loan"

class LoanStatus(Enum):
    """Loan status"""
    PENDING = "Pending"
    APPROVED = "Approved"
    ACTIVE = "Active"
    CLOSED = "Closed"
    DEFAULTED = "Defaulted"

class AccountStatus(Enum):
    """Account status"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    CLOSED = "Closed"
    FROZEN = "Frozen"

class CustomerStatus(Enum):
    """Customer status"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"

class PaymentFrequency(Enum):
    """Payment frequency for loans"""
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    HALF_YEARLY = "Half Yearly"
    YEARLY = "Yearly"

class Currency(Enum):
    """Supported currencies"""
    INR = "₹"
    USD = "$"
    EUR = "€"
    GBP = "£"

class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

class DocumentType(Enum):
    """Document types for KYC"""
    AADHAR = "Aadhar Card"
    PAN = "PAN Card"
    PASSPORT = "Passport"
    DRIVING_LICENSE = "Driving License"
    VOTER_ID = "Voter ID"

# Business Rules Constants
MIN_BALANCE = {
    AccountType.SAVINGS: 1000.0,
    AccountType.CURRENT: 5000.0,
    AccountType.FIXED_DEPOSIT: 10000.0,
    AccountType.RECURRING_DEPOSIT: 500.0
}

INTEREST_RATES = {
    AccountType.SAVINGS: 4.0,      # 4% per annum
    AccountType.CURRENT: 0.0,      # No interest
    AccountType.FIXED_DEPOSIT: 6.5, # 6.5% per annum
    AccountType.RECURRING_DEPOSIT: 5.5 # 5.5% per annum
}

LOAN_INTEREST_RATES = {
    LoanType.PERSONAL: 12.0,       # 12% per annum
    LoanType.HOME: 8.5,            # 8.5% per annum
    LoanType.CAR: 10.0,            # 10% per annum
    LoanType.EDUCATION: 7.5,       # 7.5% per annum
    LoanType.BUSINESS: 11.0        # 11% per annum
}

# Transaction limits
DAILY_WITHDRAWAL_LIMIT = 50000.0
DAILY_TRANSFER_LIMIT = 100000.0
ATM_WITHDRAWAL_LIMIT = 25000.0

# Account opening requirements
MIN_AGE_FOR_ACCOUNT = 18
MIN_INITIAL_DEPOSIT = {
    AccountType.SAVINGS: 1000.0,
    AccountType.CURRENT: 10000.0,
    AccountType.FIXED_DEPOSIT: 10000.0,
    AccountType.RECURRING_DEPOSIT: 500.0
}

# Loan limits
MAX_LOAN_AMOUNT = {
    LoanType.PERSONAL: 1000000.0,    # 10 Lakh
    LoanType.HOME: 10000000.0,       # 1 Crore
    LoanType.CAR: 2000000.0,         # 20 Lakh
    LoanType.EDUCATION: 1500000.0,   # 15 Lakh
    LoanType.BUSINESS: 5000000.0     # 50 Lakh
}

# Service charges
SERVICE_CHARGES = {
    'ATM_WITHDRAWAL_OTHER_BANK': 20.0,
    'CHEQUE_BOOK': 100.0,
    'STATEMENT_PHYSICAL': 50.0,
    'ACCOUNT_CLOSURE': 500.0,
    'INSUFFICIENT_FUNDS': 250.0,
    'SMS_ALERTS_MONTHLY': 25.0
}

# Regular expressions for validation
REGEX_PATTERNS = {
    'PAN': r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
    'AADHAR': r'^[0-9]{12}$',
    'PHONE': r'^[6-9][0-9]{9}$',
    'EMAIL': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'IFSC': r'^[A-Z]{4}[0][A-Z0-9]{6}$'
}

# Date formats
DATE_FORMATS = {
    'DISPLAY': '%d-%m-%Y',
    'DATABASE': '%Y-%m-%d',
    'DATETIME_DISPLAY': '%d-%m-%Y %H:%M:%S',
    'DATETIME_DATABASE': '%Y-%m-%d %H:%M:%S'
}

# Report types
REPORT_TYPES = [
    'Account Summary',
    'Transaction History',
    'Monthly Statement',
    'Loan Summary',
    'Interest Statement',
    'Tax Certificate',
    'Balance Certificate'
]

# Export formats
EXPORT_FORMATS = ['PDF', 'Excel', 'CSV']

# Application settings
APP_SETTINGS = {
    'APP_NAME': 'Bank Management System',
    'VERSION': '1.0.0',
    'DEVELOPER': 'Your Development Team',
    'DEFAULT_THEME': 'Default',
    'SESSION_TIMEOUT': 30,  # minutes
    'BACKUP_FREQUENCY': 7,  # days
    'LOG_RETENTION': 30,    # days
    'MAX_LOGIN_ATTEMPTS': 3
}

# Database settings
DB_SETTINGS = {
    'CONNECTION_POOL_SIZE': 10,
    'CONNECTION_TIMEOUT': 30,
    'QUERY_TIMEOUT': 300,
    'MAX_RETRIES': 3,
    'BACKUP_PATH': './backups/',
    'LOG_PATH': './logs/'
}

# GUI settings
GUI_SETTINGS = {
    'WINDOW_WIDTH': 1200,
    'WINDOW_HEIGHT': 800,
    'MIN_WIDTH': 800,
    'MIN_HEIGHT': 600,
    'FONT_FAMILY': 'Arial',
    'FONT_SIZE': 10,
    'THEME_COLORS': {
        'PRIMARY': '#2E86AB',
        'SECONDARY': '#A23B72',
        'SUCCESS': '#F18F01',
        'WARNING': '#C73E1D',
        'BACKGROUND': '#F5F5F5',
        'TEXT': '#333333'
    }
}

# Notification types
NOTIFICATION_TYPES = {
    'SUCCESS': 'success',
    'ERROR': 'error',
    'WARNING': 'warning',
    'INFO': 'info'
}

# Status messages
STATUS_MESSAGES = {
    'ACCOUNT_CREATED': 'Account created successfully',
    'ACCOUNT_UPDATED': 'Account updated successfully',
    'ACCOUNT_CLOSED': 'Account closed successfully',
    'CUSTOMER_CREATED': 'Customer created successfully',
    'CUSTOMER_UPDATED': 'Customer updated successfully',
    'TRANSACTION_SUCCESS': 'Transaction completed successfully',
    'TRANSACTION_FAILED': 'Transaction failed',
    'LOAN_APPROVED': 'Loan approved successfully',
    'LOAN_REJECTED': 'Loan application rejected',
    'PAYMENT_SUCCESS': 'Payment processed successfully',
    'INSUFFICIENT_BALANCE': 'Insufficient balance',
    'INVALID_CREDENTIALS': 'Invalid credentials',
    'SESSION_EXPIRED': 'Session expired',
    'CONNECTION_ERROR': 'Database connection error'
}

# Field lengths for database validation
FIELD_LENGTHS = {
    'CUSTOMER_NAME': 100,
    'EMAIL': 100,
    'PHONE': 15,
    'ADDRESS': 200,
    'CITY': 50,
    'STATE': 50,
    'PINCODE': 10,
    'PAN': 10,
    'AADHAR': 12,
    'ACCOUNT_NUMBER': 20,
    'IFSC': 11,
    'BRANCH_NAME': 100,
    'BRANCH_CODE': 10
}
