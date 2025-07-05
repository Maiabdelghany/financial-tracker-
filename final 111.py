import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")
        self.geometry("900x700")

        self.income = 0
        self.saving = 0
        self.expenses_list = []

        self.create_navigation()
        self.show_home()

    def create_navigation(self):
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.home_button = ttk.Button(self.nav_frame, text="Home", command=self.show_home)
        self.home_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.expenses_button = ttk.Button(self.nav_frame, text="Expenses", command=self.show_expenses)
        self.expenses_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.savings_button = ttk.Button(self.nav_frame, text="Savings", command=self.show_savings)
        self.savings_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()
        home_label = ttk.Label(self.content_frame, text="Welcome to Finance Tracker!", font=("Arial", 18))
        home_label.pack(pady=20)

        income_label = ttk.Label(self.content_frame, text="Enter your income:")
        income_label.pack()
        self.income_entry = ttk.Entry(self.content_frame)
        self.income_entry.pack()

        saving_label = ttk.Label(self.content_frame, text="Enter your savings goal:")
        saving_label.pack()
        self.saving_entry = ttk.Entry(self.content_frame)
        self.saving_entry.pack()

        submit_button = ttk.Button(self.content_frame, text="Submit", command=self.set_income_saving)
        submit_button.pack(pady=10)

    def set_income_saving(self):
        try:
            self.income = float(self.income_entry.get())
            self.saving = float(self.saving_entry.get())
            if self.saving >= self.income:
                messagebox.showerror("Error", "Savings cannot be greater than or equal to income.")
                return
            if self.saving < 0:
                messagebox.showerror("Error", "Amount must be positive.")
                return
            else:
                messagebox.showinfo("Success", "Income and savings set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def show_expenses(self):
        self.clear_frame()

        remain_income = self.income - self.saving - sum(e['amount'] for e in self.expenses_list)
        expenses_label = ttk.Label(self.content_frame, text=f"Remaining Income: ${remain_income:.2f}")
        expenses_label.pack(pady=10)

        self.expenses_listbox = tk.Listbox(self.content_frame, height=10)
        self.expenses_listbox.pack(fill=tk.BOTH, padx=10, pady=10)
        self.refresh_expenses_listbox()


        category_label = ttk.Label(self.content_frame, text="Category:")
        category_label.pack(pady=5)
        self.category_entry = ttk.Entry(self.content_frame)
        self.category_entry.pack(pady=5)

        amount_label = ttk.Label(self.content_frame, text="Amount:")
        amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(self.content_frame)
        self.amount_entry.pack(pady=5)

        save_button = ttk.Button(self.content_frame, text="Save Expense", command=self.save_expense)
        save_button.pack(pady=5)

        remove_expense_button = ttk.Button(self.content_frame, text="Remove Selected Expense", command=self.remove_expense)
        remove_expense_button.pack(pady=5)

        clear_button = ttk.Button(self.content_frame, text="Clear Expenses", command=self.clear_expenses)
        clear_button.pack(pady=5)

    def refresh_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        if not self.expenses_list:
            self.expenses_listbox.insert(tk.END, "No expenses recorded.")
        else:
            for expense in self.expenses_list:
                self.expenses_listbox.insert(
                    tk.END, f"Category: {expense['category']} - Amount: ${expense['amount']:.2f}"
                )

    def save_expense(self):
        try:
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            if not category:
                messagebox.showerror("Error", "Category cannot be empty.")
                return
            if amount < 0:
                messagebox.showerror("Error", "Amount must be positive.")
                return
            if amount >= self.income :
                messagebox.showerror("Error", "Amount cannot be greater than or equal to income.")
                return

            self.expenses_list.append({"category": category, "amount": amount})
            self.refresh_expenses_listbox()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def remove_expense(self):
        selected = self.expenses_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select an expense to remove.")
            return

        index = selected[0]
        if index < len(self.expenses_list):
            self.expenses_list.pop(index)
            self.refresh_expenses_listbox()
            messagebox.showinfo("Success", "Expense removed successfully!")

    def clear_expenses(self):
        self.expenses_list.clear()
        self.refresh_expenses_listbox()
        messagebox.showinfo("Success", "All expenses cleared.")

    def show_savings(self):
        self.clear_frame()

        total_expenses = sum(e['amount'] for e in self.expenses_list)
        remaining_income = self.income - total_expenses - self.saving
        total_savings = self.income - total_expenses

        header_label = ttk.Label(self.content_frame, text="Savings Overview", font=("Arial", 16))
        header_label.pack(pady=10)

        total_savings_label = ttk.Label(self.content_frame, text=f"Total Savings: ${total_savings:.2f}")
        total_savings_label.pack(pady=5)

        remaining_income_label = ttk.Label(self.content_frame, text=f"Remaining Income (After Expenses+Savings): ${remaining_income:.2f}")
        remaining_income_label.pack(pady=5)

        category_label = ttk.Label(self.content_frame, text="Select a category to calculate savings:")
        category_label.pack(pady=10)


        categories = [expense['category'] for expense in self.expenses_list]
        if not categories:
            categories = ["No categories available"]

        self.category_var = tk.StringVar(value="Select a category")
        category_dropdown = ttk.Combobox(self.content_frame, textvariable=self.category_var, values=categories, state="readonly")
        category_dropdown.pack(pady=5)

        amount_spent_label = ttk.Label(self.content_frame, text="Enter amount spent in the selected category:")
        amount_spent_label.pack(pady=5)

        self.amount_spent_entry = ttk.Entry(self.content_frame)
        self.amount_spent_entry.pack(pady=5)

        def calculate_savings():
            selected_category = self.category_var.get()
            if selected_category == "Select a category" or selected_category == "No categories available":
                messagebox.showerror("Error", "Please select a valid category.")
                return

            try:
                amount_spent = float(self.amount_spent_entry.get())
                category_expenses = sum(e['amount'] for e in self.expenses_list if e['category'] == selected_category)
                savings = category_expenses - amount_spent

                if savings < 0:
                    messagebox.showinfo("Savings Calculation", f"You have overspent by ${abs(savings):.2f} in {selected_category}.")
                else:
                    messagebox.showinfo("Savings Calculation", f"Saved amount for {selected_category}: ${savings:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        calculate_button = ttk.Button(self.content_frame, text="Calculate Savings", command=calculate_savings)
        calculate_button.pack(pady=10)


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
