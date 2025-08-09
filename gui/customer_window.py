"""
Customer Management Window for Bank Management System
Clean and Simple Implementation - Phase 1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.customer import Customer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CustomerWindow:
    """Simple Customer Management Window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.customer_model = Customer()
        self.window = None
        self.create_window()
        self.load_customers()
        self.load_branches()
    
    def create_window(self):
        """Create the customer management window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Customer Management")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_add_customer_tab()
        self.create_view_customers_tab()
    
    def create_add_customer_tab(self):
        """Create the Add Customer tab"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Add Customer")
        
        # Main form frame
        form_frame = ttk.LabelFrame(add_frame, text="Customer Information", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create form fields
        row = 0
        
        # First Name
        ttk.Label(form_frame, text="First Name *:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.first_name_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # Last Name
        ttk.Label(form_frame, text="Last Name *:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.last_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.last_name_var, width=30).grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Date of Birth
        ttk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.dob_var = tk.StringVar()
        self.dob_var.set("1990-01-01")
        ttk.Entry(form_frame, textvariable=self.dob_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # Gender
        ttk.Label(form_frame, text="Gender:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, 
                                   values=["MALE", "FEMALE", "OTHER"], state="readonly", width=27)
        gender_combo.grid(row=row, column=3, padx=5, pady=5)
        gender_combo.current(0)
        row += 1
        
        # Phone
        ttk.Label(form_frame, text="Phone *:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email *:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Address
        ttk.Label(form_frame, text="Address:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.address_var, width=65).grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        row += 1
        
        # City
        ttk.Label(form_frame, text="City:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.city_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.city_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # State
        ttk.Label(form_frame, text="State:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.state_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.state_var, width=30).grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Pincode
        ttk.Label(form_frame, text="Pincode:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.pincode_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pincode_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # Annual Income
        ttk.Label(form_frame, text="Annual Income:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.income_var = tk.StringVar()
        self.income_var.set("0")
        ttk.Entry(form_frame, textvariable=self.income_var, width=30).grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Occupation
        ttk.Label(form_frame, text="Occupation:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.occupation_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.occupation_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        
        # Branch
        ttk.Label(form_frame, text="Branch:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.branch_var = tk.StringVar()
        self.branch_combo = ttk.Combobox(form_frame, textvariable=self.branch_var, 
                                        state="readonly", width=27)
        self.branch_combo.grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Required fields note
        ttk.Label(form_frame, text="* Required fields", font=("Arial", 9), 
                 foreground="red").grid(row=row, column=0, columnspan=4, pady=10)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Add Customer", command=self.add_customer,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
    
    def create_view_customers_tab(self):
        """Create the View Customers tab"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Customers")
        
        # Toolbar
        toolbar = ttk.Frame(view_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.load_customers).pack(side=tk.LEFT, padx=5)
        ttk.Label(toolbar, text="Total Customers:").pack(side=tk.LEFT, padx=(20, 5))
        self.customer_count_label = ttk.Label(toolbar, text="0", font=("Arial", 10, "bold"))
        self.customer_count_label.pack(side=tk.LEFT)
        
        # Customer list
        list_frame = ttk.Frame(view_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('id', 'customer_number', 'name', 'phone', 'email', 'city', 'status')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.customer_tree.heading('id', text='ID')
        self.customer_tree.heading('customer_number', text='Customer No.')
        self.customer_tree.heading('name', text='Full Name')
        self.customer_tree.heading('phone', text='Phone')
        self.customer_tree.heading('email', text='Email')
        self.customer_tree.heading('city', text='City')
        self.customer_tree.heading('status', text='Status')
        
        # Configure column widths
        self.customer_tree.column('id', width=50)
        self.customer_tree.column('customer_number', width=150)
        self.customer_tree.column('name', width=200)
        self.customer_tree.column('phone', width=120)
        self.customer_tree.column('email', width=200)
        self.customer_tree.column('city', width=100)
        self.customer_tree.column('status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_branches(self):
        """Load available branches"""
        try:
            import mysql.connector
            from config import DB_CONFIG
            
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT branch_id, branch_name, branch_code FROM branches WHERE status = 'ACTIVE'")
            branches = cursor.fetchall()
            
            if branches:
                branch_list = [f"{branch['branch_name']} ({branch['branch_code']})" for branch in branches]
                self.branch_combo['values'] = branch_list
                
                # Store branch mapping
                self.branch_mapping = {f"{branch['branch_name']} ({branch['branch_code']})": branch['branch_id'] 
                                     for branch in branches}
                
                if branch_list:
                    self.branch_combo.current(0)
            else:
                # Create default branch if none exist
                cursor.execute("""
                    INSERT INTO branches (branch_code, branch_name, address, city, state, pincode, phone, status)
                    VALUES ('BR001', 'Main Branch', 'Main Street', 'City', 'State', '123456', '1234567890', 'ACTIVE')
                """)
                connection.commit()
                self.load_branches()  # Reload
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            logger.error(f"Error loading branches: {e}")
            # Set default values
            self.branch_combo['values'] = ['Main Branch (BR001)']
            self.branch_mapping = {'Main Branch (BR001)': 1}
            if self.branch_combo['values']:
                self.branch_combo.current(0)
    
    def load_customers(self):
        """Load all customers"""
        try:
            customers = self.customer_model.get_all_customers()
            
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Insert customer data
            for customer in customers:
                full_name = f"{customer['first_name']} {customer['last_name']}"
                self.customer_tree.insert('', 'end', values=(
                    customer['customer_id'],
                    customer['customer_number'],
                    full_name,
                    customer['phone'],
                    customer['email'],
                    customer['city'],
                    customer['status']
                ))
            
            # Update count
            self.customer_count_label.config(text=str(len(customers)))
            
        except Exception as e:
            logger.error(f"Error loading customers: {e}")
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def add_customer(self):
        """Add new customer with comprehensive validation"""
        try:
            # Get form data
            customer_data = {
                'first_name': self.first_name_var.get().strip(),
                'last_name': self.last_name_var.get().strip(),
                'date_of_birth': self.dob_var.get().strip(),
                'gender': self.gender_var.get(),
                'phone': self.phone_var.get().strip(),
                'email': self.email_var.get().strip(),
                'address': self.address_var.get().strip(),
                'city': self.city_var.get().strip(),
                'state': self.state_var.get().strip(),
                'pincode': self.pincode_var.get().strip(),
                'annual_income': float(self.income_var.get() or 0),
                'occupation': self.occupation_var.get().strip(),
                'branch_id': self.branch_mapping.get(self.branch_var.get(), 1)
            }
            
            # Validation
            if not self.validate_customer_data(customer_data):
                return
            
            # Create customer
            customer_number = self.customer_model.create_customer(customer_data)
            
            if customer_number:
                messagebox.showinfo("Success", 
                                  f"Customer created successfully!\n\n" +
                                  f"Customer Number: {customer_number}\n" +
                                  f"Name: {customer_data['first_name']} {customer_data['last_name']}")
                self.clear_form()
                self.load_customers()
            else:
                messagebox.showerror("Error", "Failed to create customer")
            
        except ValueError as e:
            messagebox.showerror("Validation Error", "Annual income must be a valid number")
        except Exception as e:
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                if "phone" in error_msg:
                    messagebox.showerror("Duplicate Data", 
                                       "A customer with this phone number already exists.\n" +
                                       "Please use a different phone number.")
                elif "email" in error_msg:
                    messagebox.showerror("Duplicate Data", 
                                       "A customer with this email address already exists.\n" +
                                       "Please use a different email address.")
                else:
                    messagebox.showerror("Duplicate Data", 
                                       "Some of the information already exists in the system.")
            else:
                logger.error(f"Error adding customer: {e}")
                messagebox.showerror("Error", f"Failed to add customer: {str(e)}")
    
    def validate_customer_data(self, data):
        """Validate customer data"""
        # Required fields
        if not all([data['first_name'], data['last_name'], data['phone'], data['email']]):
            messagebox.showerror("Validation Error", 
                               "Please fill all required fields:\n" +
                               "• First Name\n• Last Name\n• Phone\n• Email")
            return False
        
        # Phone validation
        if not data['phone'].isdigit() or len(data['phone']) != 10:
            messagebox.showerror("Validation Error", 
                               "Phone number must be exactly 10 digits")
            return False
        
        # Email validation
        if '@' not in data['email'] or '.' not in data['email']:
            messagebox.showerror("Validation Error", 
                               "Please enter a valid email address")
            return False
        
        # Date validation
        try:
            datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", 
                               "Date of birth must be in YYYY-MM-DD format\n" +
                               "Example: 1990-01-15")
            return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.dob_var.set('1990-01-01')
        self.gender_var.set('MALE')
        self.phone_var.set('')
        self.email_var.set('')
        self.address_var.set('')
        self.city_var.set('')
        self.state_var.set('')
        self.pincode_var.set('')
        self.income_var.set('0')
        self.occupation_var.set('')
        if hasattr(self, 'branch_combo') and self.branch_combo['values']:
            self.branch_combo.current(0)
