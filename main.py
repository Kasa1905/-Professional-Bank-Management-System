#!/usr/bin/env python3
"""
Bank Management System
Main Application Entry Point

A comprehensive bank management system built with Python, MySQL, and Tkinter.
Features customer manag        # Create menu buttons
        buttons = [
            ("👥 Customer Management", self.open_customer_management),
            ("💳 Account Management", self.open_account_management),
            ("💰 Transaction Processing", self.open_transaction_processing),  # Phase 3: Now active
            # ("📊 Reports & Analytics", self.open_reports),  # TODO: Implement later
            ("⚙️ Settings", self.open_settings),
            ("❌ Exit", self.exit_application)
        ]count operations, transaction processing,
loan management, and reporting capabilities.

Author: Bank Management Team
Date: July 2025
"""

import sys
import logging
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def setup_logging():
    """Setup application logging"""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bank_management.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import mysql.connector
    except ImportError:
        missing_deps.append("mysql-connector-python")
    
    if missing_deps:
        messagebox.showerror(
            "Missing Dependencies",
            f"Required packages are missing: {', '.join(missing_deps)}\n\n"
            "Please install them using:\n"
            f"pip install {' '.join(missing_deps)}"
        )
        return False
    return True

def test_database_connection():
    """Test database connection before starting the application"""
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logging.info("Database connection successful")
            connection.close()
            return True
        else:
            messagebox.showerror(
                "Database Connection Error",
                "Could not connect to the database.\n\n"
                "Please check your database configuration in config.py:\n"
                "- Ensure MySQL server is running\n"
                "- Verify host, username, and password\n"
                "- Ensure the database 'bank_management' exists"
            )
            return False
    except Exception as e:
        logging.error(f"Database connection test failed: {e}")
        messagebox.showerror(
            "Database Error",
            f"Database connection failed: {str(e)}\n\n"
            "Please check your configuration and try again."
        )
        return False

def initialize_database_if_needed():
    """Initialize database and tables if they don't exist"""
    try:
        from database_init import initialize_database
        
        logging.info("🔍 Checking and initializing database...")
        
        if initialize_database():
            logging.info("✅ Database initialization completed successfully")
            return True
        else:
            logging.error("❌ Database initialization failed")
            messagebox.showerror(
                "Database Setup Error",
                "Failed to initialize database and tables.\n\n"
                "Please check:\n"
                "- MySQL server is running\n"
                "- Database credentials in config.py are correct\n"
                "- MySQL user has CREATE privileges\n"
                "- No syntax errors in schema"
            )
            return False
            
    except Exception as e:
        logging.error(f"Database setup failed: {e}")
        messagebox.showerror(
            "Database Setup Error",
            f"Database initialization error: {str(e)}\n\n"
            "Please check your MySQL configuration and permissions."
        )
        return False

class SimpleMainWindow:
    """Simple main window for Bank Management System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_interface()
    
    def setup_window(self):
        """Setup main window"""
        self.root.title("Bank Management System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def create_interface(self):
        """Create main interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Bank Management System", 
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame, 
            text="Comprehensive Banking Solution", 
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Menu buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(expand=True)
        
        # Create menu buttons
        self.create_menu_buttons(buttons_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Database Connected")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='#34495e',
            fg='white'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu_buttons(self, parent):
        """Create main menu buttons"""
        buttons = [
            ("👥 Customer Management", self.open_customer_management),
            ("💳 Account Management", self.open_account_management),
            ("💰 Transaction Processing", self.open_transaction_processing),  # Phase 3: Complete
            ("📊 Reports & Analytics", self.open_reports),  # Next: To implement
            ("⚙️ Settings", self.open_settings),
            ("❌ Exit", self.exit_application)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                width=25,
                height=3,
                font=("Arial", 11, "bold"),
                bg='#3498db',
                fg='white',
                relief=tk.RAISED,
                bd=2,
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=20, pady=10, sticky="ew")
            
            # Button hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#2980b9'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#3498db'))
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def open_customer_management(self):
        """Open customer management window"""
        try:
            # Import here to avoid circular imports
            from gui.customer_window import CustomerWindow
            CustomerWindow(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not load Customer Management: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Customer Management: {e}")
    
    def open_account_management(self):
        """Open account management window"""
        try:
            from gui.account_window import AccountWindow
            AccountWindow(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not load Account Management: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Account Management: {e}")
    
    def open_transaction_processing(self):
        """Open transaction processing window"""
        try:
            from gui.transaction_window import TransactionWindow
            TransactionWindow(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not load Transaction Processing: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Transaction Processing: {e}")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "Settings panel - Coming Soon!")
    
    def open_reports(self):
        """Open reports window"""
        try:
            from gui.reports_window import ReportsWindow
            ReportsWindow(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not load Reports: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Reports: {e}")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "Settings panel - Coming Soon!")
    
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logging.info("Starting Bank Management System v1.0.0")
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Test database connection
    if not test_database_connection():
        return 1
    
    # Initialize database if needed
    if not initialize_database_if_needed():
        return 1
    
    try:
        # Create and run the main application
        app = SimpleMainWindow()
        logging.info("Application started successfully")
        app.run()
        logging.info("Application closed")
        return 0
        
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An unexpected error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
