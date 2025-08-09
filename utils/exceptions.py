"""
Error handling and custom exceptions for Bank Management System
"""

import logging
from typing import Optional, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bank_system.log'),
        logging.StreamHandler()
    ]
)

class BankSystemError(Exception):
    """Base exception class for Bank Management System"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 details: Optional[dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)
        
        # Log the error
        logger = logging.getLogger(__name__)
        logger.error(f"BankSystemError: {message} | Code: {error_code} | Details: {details}")

class DatabaseError(BankSystemError):
    """Database related errors"""
    pass

class ValidationError(BankSystemError):
    """Data validation errors"""
    pass

class AuthenticationError(BankSystemError):
    """Authentication related errors"""
    pass

class InsufficientBalanceError(BankSystemError):
    """Insufficient balance for transaction"""
    pass

class AccountNotFoundError(BankSystemError):
    """Account not found"""
    pass

class CustomerNotFoundError(BankSystemError):
    """Customer not found"""
    pass

class LoanError(BankSystemError):
    """Loan related errors"""
    pass

class TransactionError(BankSystemError):
    """Transaction processing errors"""
    pass

class ConfigurationError(BankSystemError):
    """Configuration related errors"""
    pass

class BusinessRuleError(BankSystemError):
    """Business rule violation errors"""
    pass

class ConnectionError(BankSystemError):
    """Database connection errors"""
    pass

class DataIntegrityError(BankSystemError):
    """Data integrity violation errors"""
    pass

class PermissionError(BankSystemError):
    """Permission/authorization errors"""
    pass

class RateLimitError(BankSystemError):
    """Rate limiting errors"""
    pass

class SessionError(BankSystemError):
    """Session management errors"""
    pass

class FileOperationError(BankSystemError):
    """File operation errors"""
    pass

class ReportGenerationError(BankSystemError):
    """Report generation errors"""
    pass

class ErrorHandler:
    """Centralized error handling utility"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_database_error(self, error: Exception, operation: str = "") -> DatabaseError:
        """Handle database errors"""
        error_msg = f"Database error during {operation}: {str(error)}"
        self.logger.error(error_msg)
        return DatabaseError(error_msg, "DB_ERROR", {"operation": operation, "original_error": str(error)})
    
    def handle_validation_error(self, field: str, value: Any, rule: str) -> ValidationError:
        """Handle validation errors"""
        error_msg = f"Validation failed for {field}: {rule}"
        self.logger.warning(error_msg)
        return ValidationError(error_msg, "VALIDATION_ERROR", 
                             {"field": field, "value": str(value), "rule": rule})
    
    def handle_insufficient_balance(self, account_number: str, required: float, 
                                  available: float) -> InsufficientBalanceError:
        """Handle insufficient balance errors"""
        error_msg = f"Insufficient balance in account {account_number}"
        self.logger.warning(error_msg)
        return InsufficientBalanceError(error_msg, "INSUFFICIENT_BALANCE",
                                      {"account": account_number, "required": required, "available": available})
    
    def handle_authentication_error(self, user_id: str = "") -> AuthenticationError:
        """Handle authentication errors"""
        error_msg = f"Authentication failed for user: {user_id}"
        self.logger.warning(error_msg)
        return AuthenticationError(error_msg, "AUTH_ERROR", {"user_id": user_id})
    
    def handle_business_rule_error(self, rule: str, details: dict = None) -> BusinessRuleError:
        """Handle business rule violations"""
        error_msg = f"Business rule violation: {rule}"
        self.logger.error(error_msg)
        return BusinessRuleError(error_msg, "BUSINESS_RULE_ERROR", details or {})
    
    def handle_connection_error(self, connection_type: str = "database") -> ConnectionError:
        """Handle connection errors"""
        error_msg = f"Connection error: {connection_type}"
        self.logger.error(error_msg)
        return ConnectionError(error_msg, "CONNECTION_ERROR", {"connection_type": connection_type})
    
    def log_transaction_error(self, transaction_type: str, account_number: str, 
                            amount: float, error: Exception):
        """Log transaction errors"""
        self.logger.error(f"Transaction failed - Type: {transaction_type}, "
                         f"Account: {account_number}, Amount: {amount}, Error: {str(error)}")
    
    def log_successful_operation(self, operation: str, details: dict = None):
        """Log successful operations"""
        self.logger.info(f"Operation successful: {operation} | Details: {details or {}}")
    
    def log_security_event(self, event_type: str, user_id: str = "", 
                          severity: str = "INFO", details: dict = None):
        """Log security events"""
        log_msg = f"Security Event - Type: {event_type}, User: {user_id}, Details: {details or {}}"
        
        if severity == "CRITICAL":
            self.logger.critical(log_msg)
        elif severity == "ERROR":
            self.logger.error(log_msg)
        elif severity == "WARNING":
            self.logger.warning(log_msg)
        else:
            self.logger.info(log_msg)

def handle_exceptions(func):
    """Decorator for handling exceptions in functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BankSystemError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            # Convert unknown exceptions to BankSystemError
            logger = logging.getLogger(__name__)
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise BankSystemError(f"Unexpected error in {func.__name__}", 
                                "UNEXPECTED_ERROR", {"function": func.__name__, "error": str(e)})
    return wrapper

def validate_and_raise(condition: bool, error_class: type, message: str, 
                      error_code: str = None, details: dict = None):
    """Validate condition and raise error if false"""
    if not condition:
        raise error_class(message, error_code, details)

def safe_execute(func, default_return=None, log_errors=True):
    """Safely execute a function and return default on error"""
    try:
        return func()
    except Exception as e:
        if log_errors:
            logger = logging.getLogger(__name__)
            logger.error(f"Error in safe_execute: {str(e)}")
        return default_return

class ErrorReporter:
    """Error reporting and metrics collection"""
    
    def __init__(self):
        self.error_counts = {}
        self.logger = logging.getLogger(__name__)
    
    def report_error(self, error: BankSystemError):
        """Report error and update metrics"""
        error_type = type(error).__name__
        
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        
        self.error_counts[error_type] += 1
        
        # Log error details
        self.logger.error(f"Error Report - Type: {error_type}, "
                         f"Message: {error.message}, Code: {error.error_code}, "
                         f"Count: {self.error_counts[error_type]}")
    
    def get_error_summary(self) -> dict:
        """Get error summary statistics"""
        return {
            "error_counts": self.error_counts.copy(),
            "total_errors": sum(self.error_counts.values()),
            "most_common_error": max(self.error_counts.items(), 
                                   key=lambda x: x[1]) if self.error_counts else None
        }
    
    def reset_metrics(self):
        """Reset error metrics"""
        self.error_counts.clear()
        self.logger.info("Error metrics reset")

# Global error handler instance
error_handler = ErrorHandler()
error_reporter = ErrorReporter()

# Error code constants
ERROR_CODES = {
    # Database errors
    'DB_CONNECTION_FAILED': 'DB001',
    'DB_QUERY_FAILED': 'DB002',
    'DB_TRANSACTION_FAILED': 'DB003',
    'DB_CONSTRAINT_VIOLATION': 'DB004',
    
    # Validation errors
    'INVALID_EMAIL': 'VAL001',
    'INVALID_PHONE': 'VAL002',
    'INVALID_AMOUNT': 'VAL003',
    'INVALID_DATE': 'VAL004',
    'REQUIRED_FIELD_MISSING': 'VAL005',
    
    # Business rule errors
    'INSUFFICIENT_BALANCE': 'BUS001',
    'ACCOUNT_INACTIVE': 'BUS002',
    'DAILY_LIMIT_EXCEEDED': 'BUS003',
    'MIN_BALANCE_VIOLATION': 'BUS004',
    'LOAN_ELIGIBILITY_FAILED': 'BUS005',
    
    # Authentication errors
    'INVALID_CREDENTIALS': 'AUTH001',
    'SESSION_EXPIRED': 'AUTH002',
    'ACCESS_DENIED': 'AUTH003',
    'ACCOUNT_LOCKED': 'AUTH004',
    
    # Transaction errors
    'TRANSACTION_FAILED': 'TXN001',
    'DUPLICATE_TRANSACTION': 'TXN002',
    'TRANSACTION_TIMEOUT': 'TXN003',
    'INVALID_TRANSACTION_TYPE': 'TXN004',
    
    # System errors
    'SYSTEM_ERROR': 'SYS001',
    'CONFIGURATION_ERROR': 'SYS002',
    'FILE_OPERATION_ERROR': 'SYS003',
    'NETWORK_ERROR': 'SYS004'
}
