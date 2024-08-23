from flask import Flask, redirect, request, render_template, url_for
from faker import Faker
import random

# Instantiate Flask application
app = Flask(__name__)

# Initialize Faker instance
fake = Faker()

# Function to generate fake transactions
def generate_fake_transactions(num_transactions=1000):
    transactions = []
    for _ in range(num_transactions):
        transaction = {
            'id': len(transactions) + 1,
            'date': fake.date_this_year(before_today=True, after_today=False).strftime('%Y-%m-%d'),
            'amount': round(random.uniform(-1000, 1000), 2)  # Random amount between -1000 and 1000
        }
        transactions.append(transaction)
    return transactions

# Generate initial fake transactions
transactions = generate_fake_transactions()

# Define routes
@app.route("/")
def get_transactions():
    # Calculate the total balance
    total_balance = sum(transaction['amount'] for transaction in transactions)
    # Render the transactions list template and pass both transactions and total balance
    return render_template("transactions.html", transactions=transactions, total_balance=f"${total_balance:.2f}")

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t['id'] != transaction_id]
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = [t for t in transactions if min_amount <= t['amount'] <= max_amount]
        # Calculate the total balance for filtered transactions
        total_balance = sum(t['amount'] for t in filtered_transactions)
        return render_template("transactions.html", transactions=filtered_transactions, total_balance=f"${total_balance:.2f}")
    return render_template("search.html")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
