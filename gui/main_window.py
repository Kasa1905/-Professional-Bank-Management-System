import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from gui.customer_window import CustomerWindow
from gui.account_window import AccountWindow
from gui.transaction_window import TransactionWindow
from gui.reports_window import ReportsWindow
from models.database import db
from config import APP_CONFIG

class MainWindow:
    """Main application window for Bank Management System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.test_database_connection()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['window_size'])
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Database Connection", command=self.show_db_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Customer menu
        customer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Customers", menu=customer_menu)
        customer_menu.add_command(label="Manage Customers", command=self.open_customer_window)
        customer_menu.add_command(label="Search Customer", command=self.search_customer)
        
        # Account menu
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Accounts", menu=account_menu)
        account_menu.add_command(label="Manage Accounts", command=self.open_account_window)
        account_menu.add_command(label="Account Balance", command=self.check_balance)
        
        # Transaction menu
        transaction_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transactions", menu=transaction_menu)
        transaction_menu.add_command(label="Process Transactions", command=self.open_transaction_window)
        transaction_menu.add_command(label="Transaction History", command=self.view_transaction_history)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Generate Reports", command=self.open_reports_window)
        reports_menu.add_command(label="Account Statement", command=self.generate_statement)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create main interface dashboard"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Bank Management System", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Quick action buttons
        self.create_quick_actions(main_frame)
        
        # Dashboard stats
        self.create_dashboard_stats(main_frame)
        
        # Recent activity
        self.create_recent_activity(main_frame)
    
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions", padding="10")
        actions_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Configure columns
        for i in range(4):
            actions_frame.columnconfigure(i, weight=1)
        
        # Action buttons
        buttons = [
            ("👤 New Customer", self.open_customer_window),
            ("🏦 New Account", self.open_account_window),
            ("💰 Transactions", self.open_transaction_window),
            ("📊 Reports", self.open_reports_window)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(actions_frame, text=text, command=command,
                           style='Action.TButton', width=15)
            btn.grid(row=0, column=i, padx=5, pady=5)
    
    def create_dashboard_stats(self, parent):
        """Create dashboard statistics"""
        stats_frame = ttk.LabelFrame(parent, text="Dashboard Statistics", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Configure columns
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # Create stat cards
        self.stat_labels = {}
        stats = [
            ("Total Customers", "customers"),
            ("Total Accounts", "accounts"),
            ("Total Balance", "balance"),
            ("Today's Transactions", "transactions")
        ]
        
        for i, (label, key) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=0, column=i, padx=10, pady=5, sticky=(tk.W, tk.E))
            
            ttk.Label(frame, text=label, style='Heading.TLabel').pack()
            self.stat_labels[key] = ttk.Label(frame, text="Loading...", 
                                            font=('Arial', 14, 'bold'))
            self.stat_labels[key].pack()
        
        # Load statistics
        self.load_dashboard_stats()
    
    def create_recent_activity(self, parent):
        """Create recent activity section"""
        activity_frame = ttk.LabelFrame(parent, text="Recent Activity", padding="10")
        activity_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Configure grid
        activity_frame.columnconfigure(0, weight=1)
        activity_frame.rowconfigure(1, weight=1)
        
        # Treeview for recent transactions
        columns = ('Time', 'Account', 'Type', 'Amount', 'Balance')
        self.activity_tree = ttk.Treeview(activity_frame, columns=columns, 
                                         show='headings', height=10)
        
        # Configure columns
        for col in columns:
            self.activity_tree.heading(col, text=col)
            if col == 'Amount' or col == 'Balance':
                self.activity_tree.column(col, width=100, anchor='e')
            else:
                self.activity_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, 
                                 command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid widgets
        self.activity_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Refresh button
        refresh_btn = ttk.Button(activity_frame, text="Refresh", 
                               command=self.load_recent_activity)
        refresh_btn.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Load recent activity
        self.load_recent_activity()
    
    def load_dashboard_stats(self):
        """Load dashboard statistics from database"""
        try:
            if not db.test_connection():
                self.stat_labels['customers'].config(text="DB Error")
                self.stat_labels['accounts'].config(text="DB Error")
                self.stat_labels['balance'].config(text="DB Error")
                self.stat_labels['transactions'].config(text="DB Error")
                return
            
            # Total customers
            customers_query = "SELECT COUNT(*) as count FROM customers WHERE status = 'ACTIVE'"
            customers_result = db.execute_query(customers_query)
            customers_count = customers_result[0]['count'] if customers_result else 0
            self.stat_labels['customers'].config(text=str(customers_count))
            
            # Total accounts
            accounts_query = "SELECT COUNT(*) as count FROM accounts WHERE status = 'ACTIVE'"
            accounts_result = db.execute_query(accounts_query)
            accounts_count = accounts_result[0]['count'] if accounts_result else 0
            self.stat_labels['accounts'].config(text=str(accounts_count))
            
            # Total balance
            balance_query = "SELECT SUM(balance) as total FROM accounts WHERE status = 'ACTIVE'"
            balance_result = db.execute_query(balance_query)
            total_balance = balance_result[0]['total'] if balance_result and balance_result[0]['total'] else 0
            self.stat_labels['balance'].config(text=f"₹{total_balance:,.2f}")
            
            # Today's transactions
            today_query = """
                SELECT COUNT(*) as count FROM transactions 
                WHERE DATE(transaction_date) = CURDATE() AND status = 'COMPLETED'
            """
            today_result = db.execute_query(today_query)
            today_count = today_result[0]['count'] if today_result else 0
            self.stat_labels['transactions'].config(text=str(today_count))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dashboard stats: {str(e)}")
    
    def load_recent_activity(self):
        """Load recent transaction activity"""
        try:
            # Clear existing items
            for item in self.activity_tree.get_children():
                self.activity_tree.delete(item)
            
            if not db.test_connection():
                return
            
            # Get recent transactions
            query = """
                SELECT 
                    t.transaction_date, a.account_number, t.transaction_type,
                    t.amount, t.balance_after
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                WHERE t.status = 'COMPLETED'
                ORDER BY t.transaction_date DESC
                LIMIT 20
            """
            
            transactions = db.execute_query(query)
            
            for transaction in transactions:
                formatted_time = transaction['transaction_date'].strftime('%H:%M:%S')
                formatted_amount = f"₹{transaction['amount']:,.2f}"
                formatted_balance = f"₹{transaction['balance_after']:,.2f}"
                
                self.activity_tree.insert('', 'end', values=(
                    formatted_time,
                    transaction['account_number'],
                    transaction['transaction_type'],
                    formatted_amount,
                    formatted_balance
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recent activity: {str(e)}")
    
    def test_database_connection(self):
        """Test database connection on startup"""
        if not db.test_connection():
            messagebox.showerror(
                "Database Connection Error",
                "Failed to connect to the database. Please check your configuration."
            )
    
    # Menu command methods
    def open_customer_window(self):
        """Open customer management window"""
        CustomerWindow(self.root)
    
    def open_account_window(self):
        """Open account management window"""
        AccountWindow(self.root)
    
    def open_transaction_window(self):
        """Open transaction processing window"""
        TransactionWindow(self.root)
    
    def open_reports_window(self):
        """Open reports window"""
        ReportsWindow(self.root)
    
    def search_customer(self):
        """Quick customer search"""
        search_term = simpledialog.askstring("Search Customer", "Enter customer name, phone, or customer number:")
        if search_term:
            from models.customer import Customer
            customer_model = Customer()
            customers = customer_model.search_customers(search_term)
            
            if customers:
                # Show results in a simple dialog
                results = "\n".join([f"{c['customer_number']} - {c['customer_name']} - {c['phone']}" for c in customers])
                messagebox.showinfo("Search Results", f"Found customers:\n\n{results}")
            else:
                messagebox.showinfo("Search Results", "No customers found.")
    
    def check_balance(self):
        """Quick balance check"""
        account_number = simpledialog.askstring("Check Balance", "Enter account number:")
        if account_number:
            from models.account import Account
            account_model = Account()
            account = account_model.get_account_by_number(account_number)
            
            if account:
                messagebox.showinfo("Account Balance", 
                    f"Account: {account['account_number']}\n"
                    f"Customer: {account['first_name']} {account['last_name']}\n"
                    f"Type: {account['account_type']}\n"
                    f"Balance: ₹{account['balance']:,.2f}")
            else:
                messagebox.showerror("Error", "Account not found.")
    
    def view_transaction_history(self):
        """Quick transaction history"""
        account_number = simpledialog.askstring("Transaction History", "Enter account number:")
        if account_number:
            from models.account import Account
            account_model = Account()
            account = account_model.get_account_by_number(account_number)
            
            if account:
                TransactionWindow(self.root, account['account_id'])
            else:
                messagebox.showerror("Error", "Account not found.")
    
    def generate_statement(self):
        """Generate account statement"""
        messagebox.showinfo("Info", "Statement generation feature will open in Reports window.")
        self.open_reports_window()
    
    def show_db_config(self):
        """Show database configuration dialog"""
        from config import DB_CONFIG
        config_info = f"""Database Configuration:
        
Host: {DB_CONFIG['host']}
Port: {DB_CONFIG['port']}
Database: {DB_CONFIG['database']}
User: {DB_CONFIG['user']}

Connection Status: {'Connected' if db.test_connection() else 'Disconnected'}"""
        
        messagebox.showinfo("Database Configuration", config_info)
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""Bank Management System
        
Version: {APP_CONFIG['version']}

A comprehensive banking application built with:
• Python 3.x
• MySQL Database
• Tkinter GUI

Features:
• Customer Management
• Account Operations
• Transaction Processing
• Loan Management
• Reports & Analytics

© 2025 Bank Management Team"""
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
