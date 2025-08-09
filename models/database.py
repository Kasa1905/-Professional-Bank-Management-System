import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import logging

class DatabaseConnection:
    """
    Database connection handler for Bank Management System
    Handles connection, error handling, and basic operations
    """
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                logging.info("Successfully connected to MySQL database")
                return True
        except Error as e:
            logging.error(f"Error connecting to MySQL database: {e}")
            return False
    
    def test_connection(self):
        """Test database connection without maintaining it"""
        try:
            test_conn = mysql.connector.connect(**DB_CONFIG)
            if test_conn.is_connected():
                test_conn.close()
                return True
            return False
        except Error as e:
            logging.error(f"Database connection test failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logging.info("MySQL connection is closed")
        except Error as e:
            logging.error(f"Error closing MySQL connection: {e}")
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute a SQL query
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            fetch (bool): Whether to fetch results
        Returns:
            list: Query results if fetch=True, else None
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
                
        except Error as e:
            logging.error(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            raise e
    
    def execute_many(self, query, params_list):
        """
        Execute a query with multiple parameter sets
        Args:
            query (str): SQL query to execute
            params_list (list): List of parameter tuples
        Returns:
            int: Number of affected rows
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return self.cursor.rowcount
            
        except Error as e:
            logging.error(f"Error executing batch query: {e}")
            if self.connection:
                self.connection.rollback()
            raise e
    
    def call_procedure(self, proc_name, args=()):
        """
        Call a stored procedure
        Args:
            proc_name (str): Name of the stored procedure
            args (tuple): Arguments for the procedure
        Returns:
            list: Procedure results
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.callproc(proc_name, args)
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            
            self.connection.commit()
            return results
            
        except Error as e:
            logging.error(f"Error calling procedure {proc_name}: {e}")
            if self.connection:
                self.connection.rollback()
            raise e
    
    def get_table_info(self, table_name):
        """Get information about a table structure"""
        query = f"DESCRIBE {table_name}"
        return self.execute_query(query)
    
    def test_connection(self):
        """Test database connection"""
        try:
            if self.connect():
                result = self.execute_query("SELECT 1 as test")
                if result and result[0]['test'] == 1:
                    return True
            return False
        except Exception as e:
            logging.error(f"Connection test failed: {e}")
            return False

# Singleton database instance
db = DatabaseConnection()
