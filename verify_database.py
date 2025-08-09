#!/usr/bin/env python3
"""
Database Verification Script
Checks if all required tables and data exist in the database
"""

import mysql.connector
from mysql.connector import Error
import logging
from config import DB_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_database():
    """Verify database setup"""
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        logger.info("🔍 Verifying database setup...")
        
        # Check if all required tables exist
        required_tables = ['branches', 'customers', 'accounts', 'transactions', 'loans', 'loan_payments', 'staff']
        
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        logger.info(f"Found tables: {existing_tables}")
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            logger.error(f"❌ Missing tables: {missing_tables}")
            return False
        else:
            logger.info("✅ All required tables exist")
        
        # Check table structures and data
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"📊 Table '{table}': {count} records")
        
        # Test basic relationships
        cursor.execute("""
            SELECT COUNT(*) 
            FROM customers c 
            JOIN branches b ON c.branch_id = b.branch_id
        """)
        customer_branch_count = cursor.fetchone()[0]
        logger.info(f"🔗 Customer-Branch relationships: {customer_branch_count}")
        
        cursor.close()
        connection.close()
        
        logger.info("✅ Database verification completed successfully")
        return True
        
    except Error as e:
        logger.error(f"❌ Database verification failed: {e}")
        return False

def test_sample_queries():
    """Test some sample queries to ensure database is working"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        logger.info("🧪 Testing sample queries...")
        
        # Test customer query
        cursor.execute("""
            SELECT 
                CONCAT(first_name, ' ', last_name) as customer_name,
                phone, email, city
            FROM customers 
            WHERE status = 'ACTIVE'
            LIMIT 3
        """)
        
        customers = cursor.fetchall()
        logger.info(f"📋 Sample customers: {len(customers)} found")
        for customer in customers:
            logger.info(f"   - {customer['customer_name']} ({customer['city']})")
        
        # Test branch query
        cursor.execute("""
            SELECT branch_name, city, manager_name
            FROM branches 
            WHERE status = 'ACTIVE'
        """)
        
        branches = cursor.fetchall()
        logger.info(f"🏢 Sample branches: {len(branches)} found")
        for branch in branches:
            logger.info(f"   - {branch['branch_name']} in {branch['city']}")
        
        cursor.close()
        connection.close()
        
        logger.info("✅ Sample queries executed successfully")
        return True
        
    except Error as e:
        logger.error(f"❌ Sample query test failed: {e}")
        return False

def main():
    """Main verification function"""
    logger.info("🚀 Bank Management System Database Verification")
    logger.info("=" * 50)
    
    # Verify database structure
    if verify_database():
        # Test sample queries
        test_sample_queries()
        
        logger.info("=" * 50)
        logger.info("🎉 Database verification completed!")
        logger.info("Your database is ready for the Bank Management System.")
    else:
        logger.error("=" * 50)
        logger.error("❌ Database verification failed!")
        logger.error("Please run: python setup_database.py")

if __name__ == "__main__":
    main()
