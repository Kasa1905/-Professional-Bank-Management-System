"""
Transaction Processing Window for Bank Management System
Phase 3 Implementation - Deposits, Withdrawals, Transfers, and History
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Transaction
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TransactionWindow:
    """Transaction Processing Window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.transaction_model = Transaction()
        self.window = None
        self.accounts = []
        self.account_mapping = {}
        self.create_window()
    
    def create_window(self):
        """Create the transaction window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Transaction Processing")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1200x800+{x}+{y}")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_deposit_tab()
        self.create_withdrawal_tab()
        self.create_transfer_tab()
        self.create_history_tab()
        
        # Load data
        self.load_data()
    
    def create_deposit_tab(self):
        """Create the Deposit tab"""
        deposit_frame = ttk.Frame(self.notebook)
        self.notebook.add(deposit_frame, text="💰 Deposit")
        
        # Title
        title_label = ttk.Label(deposit_frame, text="Cash Deposit", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(deposit_frame, text="Deposit Details", padding=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Account Selection
        ttk.Label(form_frame, text="Account *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.deposit_account_var = tk.StringVar()
        self.deposit_account_combo = ttk.Combobox(form_frame, textvariable=self.deposit_account_var,
                                                 state="readonly", width=50)
        self.deposit_account_combo.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Amount
        ttk.Label(form_frame, text="Amount *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.deposit_amount_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.deposit_amount_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.deposit_desc_var = tk.StringVar()
        self.deposit_desc_var.set("Cash Deposit")
        ttk.Entry(form_frame, textvariable=self.deposit_desc_var, width=30).grid(row=1, column=3, padx=5, pady=5)
        
        # Reference
        ttk.Label(form_frame, text="Reference:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.deposit_ref_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.deposit_ref_var, width=20).grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Process Deposit", 
                  command=self.process_deposit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_deposit_form).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
    
    def create_withdrawal_tab(self):
        """Create the Withdrawal tab"""
        withdrawal_frame = ttk.Frame(self.notebook)
        self.notebook.add(withdrawal_frame, text="💸 Withdrawal")
        
        # Title
        title_label = ttk.Label(withdrawal_frame, text="Cash Withdrawal", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(withdrawal_frame, text="Withdrawal Details", padding=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Account Selection
        ttk.Label(form_frame, text="Account *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.withdraw_account_var = tk.StringVar()
        self.withdraw_account_combo = ttk.Combobox(form_frame, textvariable=self.withdraw_account_var,
                                                  state="readonly", width=50)
        self.withdraw_account_combo.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        self.withdraw_account_combo.bind('<<ComboboxSelected>>', self.on_withdraw_account_select)
        
        # Current Balance Display
        ttk.Label(form_frame, text="Current Balance:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.withdraw_balance_var = tk.StringVar()
        self.withdraw_balance_var.set("Select account")
        ttk.Label(form_frame, textvariable=self.withdraw_balance_var, 
                 font=("Arial", 10, "bold"), foreground="blue").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Amount
        ttk.Label(form_frame, text="Amount *:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.withdraw_amount_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.withdraw_amount_var, width=20).grid(row=2, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.withdraw_desc_var = tk.StringVar()
        self.withdraw_desc_var.set("Cash Withdrawal")
        ttk.Entry(form_frame, textvariable=self.withdraw_desc_var, width=30).grid(row=2, column=3, padx=5, pady=5)
        
        # Reference
        ttk.Label(form_frame, text="Reference:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.withdraw_ref_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.withdraw_ref_var, width=20).grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Process Withdrawal", 
                  command=self.process_withdrawal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_withdrawal_form).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
    
    def create_transfer_tab(self):
        """Create the Transfer tab"""
        transfer_frame = ttk.Frame(self.notebook)
        self.notebook.add(transfer_frame, text="🔄 Transfer")
        
        # Title
        title_label = ttk.Label(transfer_frame, text="Account Transfer", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(transfer_frame, text="Transfer Details", padding=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # From Account
        ttk.Label(form_frame, text="From Account *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.transfer_from_var = tk.StringVar()
        self.transfer_from_combo = ttk.Combobox(form_frame, textvariable=self.transfer_from_var,
                                               state="readonly", width=50)
        self.transfer_from_combo.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        self.transfer_from_combo.bind('<<ComboboxSelected>>', self.on_transfer_from_select)
        
        # From Account Balance
        ttk.Label(form_frame, text="Available Balance:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.transfer_from_balance_var = tk.StringVar()
        self.transfer_from_balance_var.set("Select account")
        ttk.Label(form_frame, textvariable=self.transfer_from_balance_var,
                 font=("Arial", 10, "bold"), foreground="blue").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # To Account
        ttk.Label(form_frame, text="To Account *:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.transfer_to_var = tk.StringVar()
        self.transfer_to_combo = ttk.Combobox(form_frame, textvariable=self.transfer_to_var,
                                             state="readonly", width=50)
        self.transfer_to_combo.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Amount
        ttk.Label(form_frame, text="Amount *:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.transfer_amount_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.transfer_amount_var, width=20).grid(row=3, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        self.transfer_desc_var = tk.StringVar()
        self.transfer_desc_var.set("Account Transfer")
        ttk.Entry(form_frame, textvariable=self.transfer_desc_var, width=30).grid(row=3, column=3, padx=5, pady=5)
        
        # Reference
        ttk.Label(form_frame, text="Reference:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.transfer_ref_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.transfer_ref_var, width=20).grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Process Transfer", 
                  command=self.process_transfer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_transfer_form).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
    
    def create_history_tab(self):
        """Create the Transaction History tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📊 History")
        
        # Title
        title_label = ttk.Label(history_frame, text="Transaction History", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(history_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.load_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_transactions).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.LabelFrame(history_frame, text="Search Transactions", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self.search_transactions())
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Clear", 
                  command=self.clear_search).pack(side=tk.LEFT, padx=5)
        
        # Transaction list
        list_frame = ttk.Frame(history_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('transaction_id', 'date', 'account', 'type', 'amount', 'balance_after', 'description')
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.transaction_tree.heading('transaction_id', text='Transaction ID')
        self.transaction_tree.heading('date', text='Date')
        self.transaction_tree.heading('account', text='Account')
        self.transaction_tree.heading('type', text='Type')
        self.transaction_tree.heading('amount', text='Amount')
        self.transaction_tree.heading('balance_after', text='Balance After')
        self.transaction_tree.heading('description', text='Description')
        
        # Configure column widths
        self.transaction_tree.column('transaction_id', width=150)
        self.transaction_tree.column('date', width=120)
        self.transaction_tree.column('account', width=150)
        self.transaction_tree.column('type', width=100)
        self.transaction_tree.column('amount', width=120)
        self.transaction_tree.column('balance_after', width=120)
        self.transaction_tree.column('description', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(history_frame, text="Transaction Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(summary_frame, text="Total Transactions:").pack(side=tk.LEFT, padx=10)
        self.total_transactions_label = ttk.Label(summary_frame, text="0", font=("Arial", 10, "bold"))
        self.total_transactions_label.pack(side=tk.LEFT)
        
        ttk.Label(summary_frame, text="Total Amount:").pack(side=tk.LEFT, padx=(20, 10))
        self.total_amount_label = ttk.Label(summary_frame, text="₹0.00", font=("Arial", 10, "bold"))
        self.total_amount_label.pack(side=tk.LEFT)
    
    def load_data(self):
        """Load all necessary data"""
        self.load_accounts()
        self.load_transactions()
    
    def load_accounts(self):
        """Load accounts for dropdowns"""
        try:
            self.accounts = self.transaction_model.get_accounts_for_dropdown()
            
            if self.accounts:
                account_list = [f"{account['customer_name']} - {account['account_number']} ({account['account_type']}) - ₹{account['balance']:,.2f}" 
                               for account in self.accounts]
                
                # Update all dropdowns
                self.deposit_account_combo['values'] = account_list
                self.withdraw_account_combo['values'] = account_list
                self.transfer_from_combo['values'] = account_list
                self.transfer_to_combo['values'] = account_list
                
                # Store account mapping
                self.account_mapping = {f"{account['customer_name']} - {account['account_number']} ({account['account_type']}) - ₹{account['balance']:,.2f}": account['account_id'] 
                                      for account in self.accounts}
                
        except Exception as e:
            logger.error(f"Error loading accounts: {e}")
            messagebox.showerror("Error", f"Failed to load accounts: {str(e)}")
    
    def load_transactions(self):
        """Load all transactions"""
        try:
            print("Loading transactions...")  # Debug print
            transactions = self.transaction_model.get_all_transactions()
            print(f"Found {len(transactions)} transactions")  # Debug print
            
            # Clear existing items
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            total_amount = 0.0
            
            # Insert transaction data
            for transaction in transactions:
                amount = float(transaction['amount'] or 0)
                balance_after = float(transaction['balance_after'] or 0)
                
                # Format transaction type with emoji
                trans_type = transaction['transaction_type']
                if trans_type == 'DEPOSIT':
                    type_display = "💰 DEPOSIT"
                    total_amount += amount
                elif trans_type == 'WITHDRAWAL':
                    type_display = "💸 WITHDRAWAL" 
                    total_amount += amount
                elif trans_type == 'TRANSFER_OUT':
                    type_display = "↗️ TRANSFER OUT"
                    total_amount += amount
                elif trans_type == 'TRANSFER_IN':
                    type_display = "↘️ TRANSFER IN"
                    total_amount += amount
                else:
                    type_display = trans_type
                    total_amount += amount
                
                self.transaction_tree.insert('', 'end', values=(
                    transaction['transaction_id'],
                    transaction['transaction_date'].strftime('%Y-%m-%d %H:%M') if transaction['transaction_date'] else '',
                    transaction['account_number'] or 'N/A',
                    type_display,
                    f"₹{amount:,.2f}",
                    f"₹{balance_after:,.2f}",
                    transaction['description'] or ''
                ))
            
            # Update summary
            self.total_transactions_label.config(text=str(len(transactions)))
            self.total_amount_label.config(text=f"₹{total_amount:,.2f}")
            print(f"Loaded {len(transactions)} transactions successfully")  # Debug print
            
        except Exception as e:
            print(f"Error loading transactions: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
    
    def on_withdraw_account_select(self, event=None):
        """Update balance when withdrawal account is selected"""
        selected = self.withdraw_account_var.get()
        if selected and selected in self.account_mapping:
            account_id = self.account_mapping[selected]
            balance = self.transaction_model.get_account_balance(account_id)
            if balance is not None:
                self.withdraw_balance_var.set(f"₹{balance:,.2f}")
            else:
                self.withdraw_balance_var.set("Error getting balance")
    
    def on_transfer_from_select(self, event=None):
        """Update balance when transfer from account is selected"""
        selected = self.transfer_from_var.get()
        if selected and selected in self.account_mapping:
            account_id = self.account_mapping[selected]
            balance = self.transaction_model.get_account_balance(account_id)
            if balance is not None:
                self.transfer_from_balance_var.set(f"₹{balance:,.2f}")
            else:
                self.transfer_from_balance_var.set("Error getting balance")
    
    def process_deposit(self):
        """Process a deposit transaction"""
        try:
            selected_account = self.deposit_account_var.get()
            if not selected_account or selected_account not in self.account_mapping:
                messagebox.showerror("Error", "Please select an account")
                return
            
            amount_str = self.deposit_amount_var.get()
            if not amount_str:
                messagebox.showerror("Error", "Please enter an amount")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return
            
            account_id = self.account_mapping[selected_account]
            description = self.deposit_desc_var.get() or "Cash Deposit"
            reference = self.deposit_ref_var.get() or None
            
            print(f"Processing deposit: Account {account_id}, Amount {amount}")  # Debug print
            result = self.transaction_model.deposit(account_id, amount, description, reference)
            print(f"Deposit result: {result}")  # Debug print
            
            if result['success']:
                messagebox.showinfo("Success", result['message'] + f"\nNew Balance: ₹{result['new_balance']:,.2f}")
                self.clear_deposit_form()
                self.load_accounts()  # Refresh account balances
                self.load_transactions()  # Refresh transaction history
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Exception in process_deposit: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to process deposit: {str(e)}")
    
    def process_withdrawal(self):
        """Process a withdrawal transaction"""
        try:
            selected_account = self.withdraw_account_var.get()
            if not selected_account or selected_account not in self.account_mapping:
                messagebox.showerror("Error", "Please select an account")
                return
            
            amount_str = self.withdraw_amount_var.get()
            if not amount_str:
                messagebox.showerror("Error", "Please enter an amount")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return
            
            account_id = self.account_mapping[selected_account]
            description = self.withdraw_desc_var.get() or "Cash Withdrawal"
            reference = self.withdraw_ref_var.get() or None
            
            print(f"Processing withdrawal: Account {account_id}, Amount {amount}")  # Debug print
            result = self.transaction_model.withdraw(account_id, amount, description, reference)
            print(f"Withdrawal result: {result}")  # Debug print
            
            if result['success']:
                messagebox.showinfo("Success", result['message'] + f"\nNew Balance: ₹{result['new_balance']:,.2f}")
                self.clear_withdrawal_form()
                self.load_accounts()  # Refresh account balances
                self.load_transactions()  # Refresh transaction history
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Exception in process_withdrawal: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to process withdrawal: {str(e)}")
    
    def process_transfer(self):
        """Process a transfer transaction"""
        try:
            from_account = self.transfer_from_var.get()
            to_account = self.transfer_to_var.get()
            
            if not from_account or from_account not in self.account_mapping:
                messagebox.showerror("Error", "Please select a source account")
                return
            
            if not to_account or to_account not in self.account_mapping:
                messagebox.showerror("Error", "Please select a destination account")
                return
            
            if from_account == to_account:
                messagebox.showerror("Error", "Source and destination accounts cannot be the same")
                return
            
            amount_str = self.transfer_amount_var.get()
            if not amount_str:
                messagebox.showerror("Error", "Please enter an amount")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
                return
            
            from_account_id = self.account_mapping[from_account]
            to_account_id = self.account_mapping[to_account]
            description = self.transfer_desc_var.get() or "Account Transfer"
            reference = self.transfer_ref_var.get() or None
            
            print(f"Processing transfer: From {from_account_id} to {to_account_id}, Amount {amount}")  # Debug print
            result = self.transaction_model.transfer(from_account_id, to_account_id, amount, description, reference)
            print(f"Transfer result: {result}")  # Debug print
            
            if result['success']:
                messagebox.showinfo("Success", 
                    result['message'] + 
                    f"\nSource Balance: ₹{result['from_balance']:,.2f}" +
                    f"\nDestination Balance: ₹{result['to_balance']:,.2f}")
                self.clear_transfer_form()
                self.load_accounts()  # Refresh account balances
                self.load_transactions()  # Refresh transaction history
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Exception in process_transfer: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to process transfer: {str(e)}")
    
    def search_transactions(self):
        """Search transactions"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_transactions()  # Show all if empty
            return
        
        try:
            transactions = self.transaction_model.search_transactions(search_term)
            
            # Clear existing items
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            total_amount = 0.0
            
            # Insert search results
            for transaction in transactions:
                amount = float(transaction['amount'] or 0)
                balance_after = float(transaction['balance_after'] or 0)
                total_amount += amount
                
                # Format transaction type with emoji
                trans_type = transaction['transaction_type']
                if trans_type == 'DEPOSIT':
                    type_display = "💰 DEPOSIT"
                elif trans_type == 'WITHDRAWAL':
                    type_display = "💸 WITHDRAWAL" 
                elif trans_type == 'TRANSFER_OUT':
                    type_display = "↗️ TRANSFER OUT"
                elif trans_type == 'TRANSFER_IN':
                    type_display = "↘️ TRANSFER IN"
                else:
                    type_display = trans_type
                
                self.transaction_tree.insert('', 'end', values=(
                    transaction['transaction_id'],
                    transaction['transaction_date'].strftime('%Y-%m-%d %H:%M') if transaction['transaction_date'] else '',
                    transaction['account_number'] or 'N/A',
                    type_display,
                    f"₹{amount:,.2f}",
                    f"₹{balance_after:,.2f}",
                    transaction['description'] or ''
                ))
            
            # Update summary
            self.total_transactions_label.config(text=str(len(transactions)))
            self.total_amount_label.config(text=f"₹{total_amount:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search transactions: {str(e)}")
    
    def clear_search(self):
        """Clear search and show all transactions"""
        self.search_var.set("")
        self.load_transactions()
    
    def export_transactions(self):
        """Export transactions to CSV"""
        messagebox.showinfo("Export", "Transaction export feature - Coming Soon!")
    
    def clear_deposit_form(self):
        """Clear deposit form"""
        if self.deposit_account_combo['values']:
            self.deposit_account_combo.current(0)
        self.deposit_amount_var.set("")
        self.deposit_desc_var.set("Cash Deposit")
        self.deposit_ref_var.set("")
    
    def clear_withdrawal_form(self):
        """Clear withdrawal form"""
        if self.withdraw_account_combo['values']:
            self.withdraw_account_combo.current(0)
        self.withdraw_amount_var.set("")
        self.withdraw_desc_var.set("Cash Withdrawal")
        self.withdraw_ref_var.set("")
        self.withdraw_balance_var.set("Select account")
    
    def clear_transfer_form(self):
        """Clear transfer form"""
        if self.transfer_from_combo['values']:
            self.transfer_from_combo.current(0)
        if self.transfer_to_combo['values']:
            self.transfer_to_combo.current(0)
        self.transfer_amount_var.set("")
        self.transfer_desc_var.set("Account Transfer")
        self.transfer_ref_var.set("")
        self.transfer_from_balance_var.set("Select account")
