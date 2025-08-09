# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',  # Change this to your MySQL password
    'database': 'bank_management',
    'port': 3306,
    'charset': 'utf8mb4',
    'autocommit': True
}

# Application configuration
APP_CONFIG = {
    'title': 'Bank Management System',
    'version': '1.0.0',
    'window_size': '1200x800',
    'theme': 'default'
}

# Account types
ACCOUNT_TYPES = {
    'SAVINGS': 'Savings Account',
    'CURRENT': 'Current Account',
    'FD': 'Fixed Deposit'
}

# Transaction types
TRANSACTION_TYPES = {
    'DEPOSIT': 'Deposit',
    'WITHDRAWAL': 'Withdrawal',
    'TRANSFER': 'Transfer',
    'INTEREST': 'Interest Credit',
    'FEE': 'Service Fee'
}

# Interest rates (annual percentage)
INTEREST_RATES = {
    'SAVINGS': 4.0,
    'CURRENT': 0.0,
    'FD': 6.5
}

# Minimum balance requirements
MIN_BALANCE = {
    'SAVINGS': 1000.0,
    'CURRENT': 5000.0,
    'FD': 10000.0
}
