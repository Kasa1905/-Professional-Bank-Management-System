"""
Account Management Window for Bank Management System
Clean Implementation - Phase 2
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.account import Account
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AccountWindow:
    """Account Management Window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.account_model = Account()
        self.window = None
        self.customers = []
        self.branches = []
        self.customer_mapping = {}
        self.branch_mapping = {}
        self.create_window()
        self.load_data()
    
    def create_window(self):
        """Create the account management window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Account Management")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_add_account_tab()
        self.create_view_accounts_tab()
        self.create_search_tab()
    
    def create_add_account_tab(self):
        """Create the Add Account tab"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Create Account")
        
        # Main form frame
        form_frame = ttk.LabelFrame(add_frame, text="Account Information", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create form fields
        row = 0
        
        # Customer Selection
        ttk.Label(form_frame, text="Select Customer *:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, 
                                          state="readonly", width=50)
        self.customer_combo.grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        row += 1
        
        # Account Type
        ttk.Label(form_frame, text="Account Type *:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.account_type_var = tk.StringVar()
        account_type_combo = ttk.Combobox(form_frame, textvariable=self.account_type_var,
                                         values=["SAVINGS", "CURRENT", "FIXED_DEPOSIT", "SALARY"], 
                                         state="readonly", width=30)
        account_type_combo.grid(row=row, column=1, padx=5, pady=5)
        account_type_combo.current(0)  # Default to SAVINGS
        
        # Initial Balance
        ttk.Label(form_frame, text="Initial Balance:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.initial_balance_var = tk.StringVar()
        self.initial_balance_var.set("0.00")
        ttk.Entry(form_frame, textvariable=self.initial_balance_var, width=30).grid(row=row, column=3, padx=5, pady=5)
        row += 1
        
        # Account Number (Auto-generated)
        ttk.Label(form_frame, text="Account Number:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.account_number_var = tk.StringVar()
        self.account_number_var.set("(Auto-generated)")
        account_number_entry = ttk.Entry(form_frame, textvariable=self.account_number_var, 
                                        state="readonly", width=30)
        account_number_entry.grid(row=row, column=1, padx=5, pady=5)
        
        # Generate Account Number Button
        ttk.Button(form_frame, text="Generate Account Number", 
                  command=self.generate_account_number).grid(row=row, column=2, padx=5, pady=5)
        row += 1
        
        # Required fields note
        ttk.Label(form_frame, text="* Required fields", font=("Arial", 9), 
                 foreground="red").grid(row=row, column=0, columnspan=4, pady=10)
        row += 1
        
        # Information frame
        info_frame = ttk.LabelFrame(form_frame, text="Account Types Information", padding=10)
        info_frame.grid(row=row, column=0, columnspan=4, sticky=tk.W+tk.E, pady=10)
        
        info_text = """
        • SAVINGS: Regular savings account with interest
        • CURRENT: Business/checking account for transactions
        • FIXED_DEPOSIT: Time deposit with higher interest rates
        • SALARY: Salary account for employees
        """
        ttk.Label(info_frame, text=info_text, font=("Arial", 9)).pack(anchor=tk.W)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Create Account", command=self.create_account,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Refresh Customer List", 
                  command=self.load_customers).pack(side=tk.LEFT, padx=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
    
    def create_view_accounts_tab(self):
        """Create the View Accounts tab"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Accounts")
        
        # Toolbar
        toolbar = ttk.Frame(view_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.load_accounts).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Close Selected Account", 
                  command=self.close_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Reactivate Selected Account", 
                  command=self.reactivate_account).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(toolbar, text="Total Accounts:").pack(side=tk.LEFT, padx=(20, 5))
        self.account_count_label = ttk.Label(toolbar, text="0", font=("Arial", 10, "bold"))
        self.account_count_label.pack(side=tk.LEFT)
        
        ttk.Label(toolbar, text="Total Balance:").pack(side=tk.LEFT, padx=(20, 5))
        self.total_balance_label = ttk.Label(toolbar, text="₹0.00", font=("Arial", 10, "bold"))
        self.total_balance_label.pack(side=tk.LEFT)
        
        # Account list
        list_frame = ttk.Frame(view_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('id', 'account_number', 'customer_name', 'account_type', 'balance', 'status')
        self.account_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.account_tree.heading('id', text='ID')
        self.account_tree.heading('account_number', text='Account Number')
        self.account_tree.heading('customer_name', text='Customer Name')
        self.account_tree.heading('account_type', text='Account Type')
        self.account_tree.heading('balance', text='Balance')
        self.account_tree.heading('status', text='Status')
        
        # Configure column widths
        self.account_tree.column('id', width=50)
        self.account_tree.column('account_number', width=150)
        self.account_tree.column('customer_name', width=200)
        self.account_tree.column('account_type', width=120)
        self.account_tree.column('balance', width=120)
        self.account_tree.column('status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.account_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_search_tab(self):
        """Create the Search Accounts tab"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search Accounts")
        
        # Search controls
        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_controls, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_controls, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_accounts())
        
        ttk.Button(search_controls, text="Search", command=self.search_accounts).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_controls, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=5)
        
        # Search results
        search_list_frame = ttk.Frame(search_frame)
        search_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Search treeview
        columns = ('id', 'account_number', 'customer_name', 'account_type', 'balance', 'status')
        self.search_tree = ttk.Treeview(search_list_frame, columns=columns, show='headings', height=20)
        
        # Define headings (same as main view)
        for col in columns:
            self.search_tree.heading(col, text=self.account_tree.heading(col)['text'])
            self.search_tree.column(col, width=self.account_tree.column(col)['width'])
        
        # Search scrollbar
        search_scrollbar = ttk.Scrollbar(search_list_frame, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=search_scrollbar.set)
        
        # Pack
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        search_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_data(self):
        """Load all necessary data"""
        self.load_customers()
        self.load_accounts()
    
    def load_customers(self):
        """Load customers for dropdown"""
        try:
            self.customers = self.account_model.get_customers_for_dropdown()
            
            if self.customers:
                customer_list = [f"{customer['customer_number']} - {customer['first_name']} {customer['last_name']}" 
                               for customer in self.customers]
                self.customer_combo['values'] = customer_list
                
                # Store customer mapping
                self.customer_mapping = {f"{customer['customer_number']} - {customer['first_name']} {customer['last_name']}": customer['customer_id'] 
                                       for customer in self.customers}
                
                if customer_list:
                    self.customer_combo.current(0)
            else:
                messagebox.showwarning("No Customers", 
                                     "No active customers found. Please add customers first.")
                self.customer_combo['values'] = []
                
        except Exception as e:
            logger.error(f"Error loading customers: {e}")
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def load_branches(self):
        """Load branches for dropdown"""
        # Branches not used in simplified version
        self.branches = []
        self.branch_mapping = {}
    
    def load_accounts(self):
        """Load all accounts"""
        try:
            print("Loading accounts...")  # Debug print
            accounts = self.account_model.get_all_accounts()
            print(f"Found {len(accounts)} accounts")  # Debug print
            
            # Clear existing items
            for item in self.account_tree.get_children():
                self.account_tree.delete(item)
            
            total_balance = 0.0
            
            # Insert account data
            for account in accounts:
                balance = float(account['balance'] or 0)
                total_balance += balance
                
                # Format status to make closed accounts more visible
                status_display = account['status']
                if account['status'] == 'CLOSED':
                    status_display = "🚫 CLOSED"
                elif account['status'] == 'ACTIVE':
                    status_display = "✅ ACTIVE"
                elif account['status'] == 'INACTIVE':
                    status_display = "⏸️ INACTIVE"
                
                item = self.account_tree.insert('', 'end', values=(
                    account['account_id'],
                    account['account_number'],
                    account['customer_name'] or 'N/A',
                    account.get('account_type_display', account['account_type']),  # Use display type if available
                    f"₹{balance:,.2f}",
                    status_display
                ))
                
                # Color code closed accounts (gray out)
                if account['status'] == 'CLOSED':
                    self.account_tree.set(item, 'account_number', f"[CLOSED] {account['account_number']}")
                    # Note: Tkinter Treeview doesn't support row colors easily, but we added prefix
            
            # Update counts and totals
            self.account_count_label.config(text=str(len(accounts)))
            self.total_balance_label.config(text=f"₹{total_balance:,.2f}")
            print(f"Loaded {len(accounts)} accounts successfully")  # Debug print
            
        except Exception as e:
            print(f"Error loading accounts: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load accounts: {str(e)}")
    
    def generate_account_number(self):
        """Generate a new account number"""
        account_number = self.account_model.generate_account_number()
        self.account_number_var.set(account_number)
    
    def create_account(self):
        """Create new account with validation"""
        try:
            # Get form data
            selected_customer = self.customer_var.get()
            customer_id = self.customer_mapping.get(selected_customer)
            
            account_data = {
                'customer_id': customer_id,
                'account_type': self.account_type_var.get(),
                'initial_balance': float(self.initial_balance_var.get() or 0)
            }
            
            # Add custom account number if generated
            if self.account_number_var.get() != "(Auto-generated)":
                account_data['account_number'] = self.account_number_var.get()
            
            # Validation
            if not self.validate_account_data(account_data):
                return
            
            # Create account
            account_number = self.account_model.create_account(account_data)
            
            if account_number:
                customer_name = selected_customer.split(' - ')[1] if ' - ' in selected_customer else 'Customer'
                messagebox.showinfo("Success", 
                                  f"Account created successfully!\n\n" +
                                  f"Account Number: {account_number}\n" +
                                  f"Customer: {customer_name}\n" +
                                  f"Account Type: {account_data['account_type']}\n" +
                                  f"Initial Balance: ₹{account_data['initial_balance']:,.2f}")
                self.clear_form()
                self.load_accounts()
            else:
                messagebox.showerror("Error", "Failed to create account")
            
        except ValueError as e:
            messagebox.showerror("Validation Error", "Initial balance must be a valid number")
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")
    
    def validate_account_data(self, data):
        """Validate account data"""
        # Required fields
        if not data.get('customer_id'):
            messagebox.showerror("Validation Error", "Please select a customer")
            return False
        
        if not data.get('account_type'):
            messagebox.showerror("Validation Error", "Please select an account type")
            return False
        
        # Balance validation
        if data['initial_balance'] < 0:
            messagebox.showerror("Validation Error", "Initial balance cannot be negative")
            return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        if self.customer_combo['values']:
            self.customer_combo.current(0)
        self.account_type_var.set('SAVINGS')
        self.initial_balance_var.set('0.00')
        self.account_number_var.set('(Auto-generated)')
    
    def close_account(self):
        """Close selected account"""
        selection = self.account_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account to close")
            return
        
        account_id = self.account_tree.item(selection[0])['values'][0]
        account_number = self.account_tree.item(selection[0])['values'][1]
        customer_name = self.account_tree.item(selection[0])['values'][2]
        current_status = self.account_tree.item(selection[0])['values'][5]
        
        # Check if account is already closed
        if current_status == 'CLOSED':
            messagebox.showinfo("Info", "This account is already closed.")
            return
        
        if messagebox.askyesno("Confirm Close", 
                              f"Are you sure you want to close this account?\n\n" +
                              f"Account: {account_number}\n" +
                              f"Customer: {customer_name}\n" +
                              f"Current Status: {current_status}"):
            try:
                print(f"Attempting to close account ID: {account_id}")  # Debug print
                result = self.account_model.update_account_status(account_id, 'CLOSED')
                print(f"Close account result: {result}")  # Debug print
                
                if result:
                    messagebox.showinfo("Success", 
                                      f"Account closed successfully!\n\n" +
                                      f"Account: {account_number}\n" +
                                      f"Status changed to: CLOSED")
                    self.load_accounts()  # Refresh the view
                else:
                    messagebox.showerror("Error", "Failed to close account. Please try again.")
            except Exception as e:
                print(f"Exception in close_account: {e}")  # Debug print
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to close account: {str(e)}")
    
    def reactivate_account(self):
        """Reactivate a closed account"""
        selection = self.account_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account to reactivate")
            return
        
        account_id = self.account_tree.item(selection[0])['values'][0]
        account_number = self.account_tree.item(selection[0])['values'][1]
        customer_name = self.account_tree.item(selection[0])['values'][2]
        current_status = self.account_tree.item(selection[0])['values'][5]
        
        # Check if account is not closed
        if 'CLOSED' not in current_status:
            messagebox.showinfo("Info", "This account is already active or not closed.")
            return
        
        if messagebox.askyesno("Confirm Reactivation", 
                              f"Are you sure you want to reactivate this account?\n\n" +
                              f"Account: {account_number}\n" +
                              f"Customer: {customer_name}"):
            try:
                print(f"Attempting to reactivate account ID: {account_id}")  # Debug print
                result = self.account_model.update_account_status(account_id, 'ACTIVE')
                print(f"Reactivate account result: {result}")  # Debug print
                
                if result:
                    messagebox.showinfo("Success", 
                                      f"Account reactivated successfully!\n\n" +
                                      f"Account: {account_number}\n" +
                                      f"Status changed to: ACTIVE")
                    self.load_accounts()  # Refresh the view
                else:
                    messagebox.showerror("Error", "Failed to reactivate account. Please try again.")
            except Exception as e:
                print(f"Exception in reactivate_account: {e}")  # Debug print
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to reactivate account: {str(e)}")
    
    def search_accounts(self):
        """Search accounts"""
        search_term = self.search_var.get().strip()
        if not search_term:
            # Clear search results
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            return
        
        try:
            accounts = self.account_model.search_accounts(search_term)
            
            # Clear existing items
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            
            # Insert search results
            for account in accounts:
                balance = float(account['balance'] or 0)
                
                self.search_tree.insert('', 'end', values=(
                    account['account_id'],
                    account['account_number'],
                    account['customer_name'] or 'N/A',
                    account.get('account_type_display', account['account_type']),  # Use display type if available
                    f"₹{balance:,.2f}",
                    account['status']
                ))
                
        except Exception as e:
            logger.error(f"Error searching accounts: {e}")
            messagebox.showerror("Error", f"Failed to search accounts: {str(e)}")
    
    def clear_search(self):
        """Clear search"""
        self.search_var.set('')
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
