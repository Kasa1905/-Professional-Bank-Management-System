"""
Reports and Analytics Window for Bank Management System
Complete Implementation with Database Integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import logging
import csv
import os
from models.customer import Customer
from models.account import Account 
from models.transaction import Transaction

logger = logging.getLogger(__name__)

class ReportsWindow:
    """Reports and analytics window with full functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.customer_model = Customer()
        self.account_model = Account()
        self.transaction_model = Transaction()
        self.create_window()
    
    def create_window(self):
        """Create the reports window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Reports & Analytics")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1200x700+{x}+{y}")

        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Reports & Analytics Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different report categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_summary_reports_tab()
        self.create_transaction_reports_tab()
        self.create_customer_reports_tab()
        self.create_analytics_tab()
    
    def create_summary_reports_tab(self):
        """Create the Summary Reports tab"""
    
    def create_summary_reports_tab(self):
        """Create the Summary Reports tab"""
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="📊 Summary")
        
        # Create summary cards
        self.create_summary_cards(summary_frame)
        
        # Quick reports section
        reports_frame = ttk.LabelFrame(summary_frame, text="Quick Reports", padding=10)
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        quick_reports = [
            ("System Overview", self.generate_system_overview, "Get overall system statistics"),
            ("Daily Summary", self.generate_daily_summary, "Today's transactions and activities"),
            ("Account Status Report", self.generate_account_status, "Active, inactive, and closed accounts"),
            ("Customer Demographics", self.generate_customer_demographics, "Customer analysis by location, age, etc.")
        ]
        
        row = 0
        for report_name, command, description in quick_reports:
            frame = ttk.Frame(reports_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(frame, text=report_name, command=command, width=25).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=description, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
    
    def create_transaction_reports_tab(self):
        """Create the Transaction Reports tab"""
        transaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(transaction_frame, text="💰 Transactions")
        
        # Date range selection
        date_frame = ttk.LabelFrame(transaction_frame, text="Date Range", padding=10)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, padx=5, pady=5)
        self.from_date_var = tk.StringVar()
        self.from_date_var.set((datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.from_date_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(date_frame, text="To:").grid(row=0, column=2, padx=5, pady=5)
        self.to_date_var = tk.StringVar()
        self.to_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.to_date_var, width=15).grid(row=0, column=3, padx=5, pady=5)
        
        # Transaction reports
        trans_reports_frame = ttk.LabelFrame(transaction_frame, text="Transaction Reports", padding=10)
        trans_reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        transaction_reports = [
            ("Transaction History", self.generate_transaction_history, "Complete transaction log with filters"),
            ("Daily Transaction Summary", self.generate_daily_transactions, "Transactions grouped by day"),
            ("Monthly Analysis", self.generate_monthly_analysis, "Monthly transaction trends"),
            ("Account Activity Report", self.generate_account_activity, "Per-account transaction summary"),
            ("Large Transactions", self.generate_large_transactions, "Transactions above specified amount")
        ]
        
        for report_name, command, description in transaction_reports:
            frame = ttk.Frame(trans_reports_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(frame, text=report_name, command=command, width=25).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=description, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
    
    def create_customer_reports_tab(self):
        """Create the Customer Reports tab"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="👥 Customers")
        
        # Customer reports
        customer_reports_frame = ttk.LabelFrame(customer_frame, text="Customer Reports", padding=10)
        customer_reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        customer_reports = [
            ("Customer List", self.generate_customer_list, "Complete list of all customers"),
            ("New Customers", self.generate_new_customers, "Recently registered customers"),
            ("Customer Account Summary", self.generate_customer_accounts, "Customers with their accounts"),
            ("Inactive Customers", self.generate_inactive_customers, "Customers with no recent activity"),
            ("Customer Balance Report", self.generate_customer_balances, "Customer total balances across accounts")
        ]
        
        for report_name, command, description in customer_reports:
            frame = ttk.Frame(customer_reports_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(frame, text=report_name, command=command, width=25).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=description, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
    
    def create_analytics_tab(self):
        """Create the Analytics tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📈 Analytics")
        
        # Analytics section
        analytics_reports_frame = ttk.LabelFrame(analytics_frame, text="Business Analytics", padding=10)
        analytics_reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        analytics_reports = [
            ("Growth Analysis", self.generate_growth_analysis, "Customer and account growth trends"),
            ("Revenue Analysis", self.generate_revenue_analysis, "Transaction volume and patterns"),
            ("Account Type Distribution", self.generate_account_distribution, "Breakdown by account types"),
            ("Seasonal Trends", self.generate_seasonal_trends, "Transaction patterns by month/season"),
            ("Risk Assessment", self.generate_risk_assessment, "Large withdrawals and dormant accounts")
        ]
        
        for report_name, command, description in analytics_reports:
            frame = ttk.Frame(analytics_reports_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(frame, text=report_name, command=command, width=25).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=description, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
    
    def create_summary_cards(self, parent):
        """Create summary cards showing key metrics"""
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Get summary data
        try:
            customers = self.customer_model.get_all_customers()
            accounts = self.account_model.get_all_accounts()
            
            total_customers = len(customers)
            total_accounts = len(accounts)
            total_balance = sum(float(acc.get('balance', 0)) for acc in accounts)
            active_accounts = len([acc for acc in accounts if acc.get('status') == 'ACTIVE'])
            
        except Exception as e:
            logger.error(f"Error getting summary data: {e}")
            total_customers = total_accounts = active_accounts = 0
            total_balance = 0.0
        
        # Create cards
        cards_data = [
            ("Total Customers", f"{total_customers:,}", "👥", "#3498db"),
            ("Total Accounts", f"{total_accounts:,}", "💳", "#e74c3c"),
            ("Active Accounts", f"{active_accounts:,}", "✅", "#27ae60"),
            ("Total Balance", f"₹{total_balance:,.2f}", "💰", "#f39c12")
        ]
        
        for i, (title, value, icon, color) in enumerate(cards_data):
            card = ttk.LabelFrame(cards_frame, text=" ")
            card.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            
            # Icon and title
            title_frame = ttk.Frame(card)
            title_frame.pack(pady=5)
            ttk.Label(title_frame, text=icon, font=("Arial", 20)).pack()
            ttk.Label(title_frame, text=title, font=("Arial", 10)).pack()
            
            # Value
            ttk.Label(card, text=value, font=("Arial", 14, "bold"), 
                     foreground=color).pack(pady=5)
        
        # Configure grid weights
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
    
    # Report Generation Methods
    
    def generate_system_overview(self):
        """Generate system overview report"""
        try:
            customers = self.customer_model.get_all_customers()
            accounts = self.account_model.get_all_accounts()
            
            report_data = []
            report_data.append("=" * 60)
            report_data.append("BANK MANAGEMENT SYSTEM - OVERVIEW REPORT")
            report_data.append("=" * 60)
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")
            
            # Customer Statistics
            report_data.append("CUSTOMER STATISTICS:")
            report_data.append("-" * 20)
            report_data.append(f"Total Customers: {len(customers)}")
            active_customers = len([c for c in customers if c.get('status') == 'ACTIVE'])
            report_data.append(f"Active Customers: {active_customers}")
            report_data.append("")
            
            # Account Statistics
            report_data.append("ACCOUNT STATISTICS:")
            report_data.append("-" * 20)
            report_data.append(f"Total Accounts: {len(accounts)}")
            
            account_types = {}
            active_accounts = 0
            total_balance = 0.0
            
            for acc in accounts:
                acc_type = acc.get('account_type', 'UNKNOWN')
                account_types[acc_type] = account_types.get(acc_type, 0) + 1
                
                if acc.get('status') == 'ACTIVE':
                    active_accounts += 1
                
                balance = float(acc.get('balance', 0))
                total_balance += balance
            
            report_data.append(f"Active Accounts: {active_accounts}")
            report_data.append(f"Total Balance: ₹{total_balance:,.2f}")
            report_data.append("")
            
            report_data.append("ACCOUNT TYPES BREAKDOWN:")
            report_data.append("-" * 25)
            for acc_type, count in account_types.items():
                report_data.append(f"{acc_type}: {count}")
            
            # Display or save report
            self.show_report_dialog("System Overview", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating system overview: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_daily_summary(self):
        """Generate daily summary report"""
        try:
            today = datetime.now().date()
            transactions = self.transaction_model.get_all_transactions()
            
            # Filter today's transactions
            today_transactions = []
            for trans in transactions:
                trans_date = trans.get('transaction_date')
                if trans_date and trans_date.date() == today:
                    today_transactions.append(trans)
            
            report_data = []
            report_data.append("=" * 60)
            report_data.append("DAILY SUMMARY REPORT")
            report_data.append("=" * 60)
            report_data.append(f"Date: {today.strftime('%Y-%m-%d')}")
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")
            
            if not today_transactions:
                report_data.append("No transactions found for today.")
            else:
                # Analyze transactions
                deposits = [t for t in today_transactions if t.get('transaction_type') == 'DEPOSIT']
                withdrawals = [t for t in today_transactions if t.get('transaction_type') == 'WITHDRAWAL']
                transfers_out = [t for t in today_transactions if t.get('transaction_type') == 'TRANSFER_OUT']
                transfers_in = [t for t in today_transactions if t.get('transaction_type') == 'TRANSFER_IN']
                
                total_deposits = sum(float(t.get('amount', 0)) for t in deposits)
                total_withdrawals = sum(float(t.get('amount', 0)) for t in withdrawals)
                total_transfers = sum(float(t.get('amount', 0)) for t in transfers_out)
                
                report_data.append("TRANSACTION SUMMARY:")
                report_data.append("-" * 20)
                report_data.append(f"Total Transactions: {len(today_transactions)}")
                report_data.append(f"Deposits: {len(deposits)} (₹{total_deposits:,.2f})")
                report_data.append(f"Withdrawals: {len(withdrawals)} (₹{total_withdrawals:,.2f})")
                report_data.append(f"Transfers: {len(transfers_out)} (₹{total_transfers:,.2f})")
                report_data.append("")
                
                net_flow = total_deposits - total_withdrawals
                report_data.append(f"Net Cash Flow: ₹{net_flow:,.2f}")
            
            self.show_report_dialog("Daily Summary", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_account_status(self):
        """Generate account status report"""
        try:
            accounts = self.account_model.get_all_accounts()
            
            report_data = []
            report_data.append("=" * 60)
            report_data.append("ACCOUNT STATUS REPORT")
            report_data.append("=" * 60)
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")
            
            # Group by status
            status_groups = {}
            for acc in accounts:
                status = acc.get('status', 'UNKNOWN')
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(acc)
            
            for status, acc_list in status_groups.items():
                report_data.append(f"{status} ACCOUNTS ({len(acc_list)}):")
                report_data.append("-" * (len(status) + 12))
                
                total_balance = 0.0
                for acc in acc_list:
                    balance = float(acc.get('balance', 0))
                    total_balance += balance
                    report_data.append(f"  {acc.get('account_number', 'N/A')} - {acc.get('customer_name', 'N/A')} - ₹{balance:,.2f}")
                
                report_data.append(f"  Total Balance: ₹{total_balance:,.2f}")
                report_data.append("")
            
            self.show_report_dialog("Account Status Report", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating account status report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_customer_demographics(self):
        """Generate customer demographics report"""
        try:
            customers = self.customer_model.get_all_customers()
            
            report_data = []
            report_data.append("=" * 60)
            report_data.append("CUSTOMER DEMOGRAPHICS REPORT")
            report_data.append("=" * 60)
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")
            
            # City distribution
            cities = {}
            for customer in customers:
                city = customer.get('city', 'Unknown')
                cities[city] = cities.get(city, 0) + 1
            
            report_data.append("CUSTOMERS BY CITY:")
            report_data.append("-" * 20)
            for city, count in sorted(cities.items()):
                report_data.append(f"{city}: {count}")
            report_data.append("")
            
            # Status distribution
            statuses = {}
            for customer in customers:
                status = customer.get('status', 'Unknown')
                statuses[status] = statuses.get(status, 0) + 1
            
            report_data.append("CUSTOMERS BY STATUS:")
            report_data.append("-" * 21)
            for status, count in statuses.items():
                report_data.append(f"{status}: {count}")
            
            self.show_report_dialog("Customer Demographics", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating customer demographics: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_transaction_history(self):
        """Generate transaction history report with date filter"""
        try:
            from_date = datetime.strptime(self.from_date_var.get(), "%Y-%m-%d").date()
            to_date = datetime.strptime(self.to_date_var.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dates in YYYY-MM-DD format")
            return
        
        try:
            all_transactions = self.transaction_model.get_all_transactions()
            
            # Filter by date range
            filtered_transactions = []
            for trans in all_transactions:
                trans_date = trans.get('transaction_date')
                if trans_date and from_date <= trans_date.date() <= to_date:
                    filtered_transactions.append(trans)
            
            report_data = []
            report_data.append("=" * 80)
            report_data.append("TRANSACTION HISTORY REPORT")
            report_data.append("=" * 80)
            report_data.append(f"Period: {from_date} to {to_date}")
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append("")
            
            if not filtered_transactions:
                report_data.append("No transactions found for the selected period.")
            else:
                report_data.append(f"Total Transactions: {len(filtered_transactions)}")
                report_data.append("")
                report_data.append(f"{'Date':<12} {'Account':<15} {'Type':<12} {'Amount':<15} {'Balance':<15} {'Description':<20}")
                report_data.append("-" * 80)
                
                for trans in filtered_transactions:
                    date_str = trans.get('transaction_date', '').strftime('%Y-%m-%d') if trans.get('transaction_date') else 'N/A'
                    account = trans.get('account_number', 'N/A')[:12]
                    trans_type = trans.get('transaction_type', 'N/A')[:10]
                    amount = f"₹{float(trans.get('amount', 0)):,.2f}"
                    balance = f"₹{float(trans.get('balance_after', 0)):,.2f}"
                    desc = (trans.get('description', 'N/A')[:18] + '..') if len(str(trans.get('description', ''))) > 20 else str(trans.get('description', 'N/A'))
                    
                    report_data.append(f"{date_str:<12} {account:<15} {trans_type:<12} {amount:<15} {balance:<15} {desc:<20}")
            
            self.show_report_dialog("Transaction History", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating transaction history: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_customer_list(self):
        """Generate complete customer list"""
        try:
            customers = self.customer_model.get_all_customers()
            
            report_data = []
            report_data.append("=" * 80)
            report_data.append("CUSTOMER LIST REPORT")
            report_data.append("=" * 80)
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_data.append(f"Total Customers: {len(customers)}")
            report_data.append("")
            
            if customers:
                report_data.append(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'City':<15} {'Status':<8}")
                report_data.append("-" * 80)
                
                for customer in customers:
                    cust_id = str(customer.get('customer_id', 'N/A'))
                    name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}"[:23]
                    phone = customer.get('phone', 'N/A')[:13]
                    city = customer.get('city', 'N/A')[:13]
                    status = customer.get('status', 'N/A')
                    
                    report_data.append(f"{cust_id:<5} {name:<25} {phone:<15} {city:<15} {status:<8}")
            else:
                report_data.append("No customers found.")
            
            self.show_report_dialog("Customer List", "\n".join(report_data))
            
        except Exception as e:
            logger.error(f"Error generating customer list: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def show_report_dialog(self, title, content):
        """Show report in a dialog with export option"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Report: {title}")
        dialog.geometry("900x600")
        
        # Text area with scrollbar
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_area = tk.Text(text_frame, wrap=tk.NONE, font=("Courier", 10))
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_area.xview)
        
        text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Insert content
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Export to File", 
                  command=lambda: self.export_report(title, content)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def export_report(self, title, content):
        """Export report to text file"""
        try:
            # Create reports directory if it doesn't exist
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{title.replace(' ', '_')}_{timestamp}.txt"
            filepath = os.path.join(reports_dir, filename)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Success", f"Report exported to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    # Placeholder methods for additional reports
    def generate_daily_transactions(self):
        messagebox.showinfo("Report", "Daily Transaction Summary - Under Development!")
    
    def generate_monthly_analysis(self):
        messagebox.showinfo("Report", "Monthly Analysis - Under Development!")
    
    def generate_account_activity(self):
        messagebox.showinfo("Report", "Account Activity Report - Under Development!")
    
    def generate_large_transactions(self):
        messagebox.showinfo("Report", "Large Transactions Report - Under Development!")
    
    def generate_new_customers(self):
        messagebox.showinfo("Report", "New Customers Report - Under Development!")
    
    def generate_customer_accounts(self):
        messagebox.showinfo("Report", "Customer Account Summary - Under Development!")
    
    def generate_inactive_customers(self):
        messagebox.showinfo("Report", "Inactive Customers Report - Under Development!")
    
    def generate_customer_balances(self):
        messagebox.showinfo("Report", "Customer Balance Report - Under Development!")
    
    def generate_growth_analysis(self):
        messagebox.showinfo("Report", "Growth Analysis - Under Development!")
    
    def generate_revenue_analysis(self):
        messagebox.showinfo("Report", "Revenue Analysis - Under Development!")
    
    def generate_account_distribution(self):
        messagebox.showinfo("Report", "Account Distribution - Under Development!")
    
    def generate_seasonal_trends(self):
        messagebox.showinfo("Report", "Seasonal Trends - Under Development!")
    
    def generate_risk_assessment(self):
        messagebox.showinfo("Report", "Risk Assessment - Under Development!")