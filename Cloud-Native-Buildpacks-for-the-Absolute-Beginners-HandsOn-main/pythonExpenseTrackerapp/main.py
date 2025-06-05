import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
from models.expense import Expense
from models.category import Category
from datetime import datetime
from urllib.parse import unquote
import os
import mimetypes

# Database connection setup
try:
    conn = psycopg2.connect(
        dbname="expense_tracker",        # Replace with your database name
        user="postgres",              # Default PostgreSQL user
        password="root",     # Replace with your password
        host="expense_tracker",             # Server address
        port="5432"                   # PostgreSQL default port
    )
    cursor = conn.cursor()
    print("Connected to the database successfully!")
except psycopg2.OperationalError as e:
    print(f"Failed to connect to the database: {e}")
    exit(1)

# Global list to hold expenses
expenses = []

# Define list of categories
categories = ["Food", "Health", "Transport", "Miscellaneous"]

# Load expenses from the PostgreSQL database
def load_expenses():
    global expenses
    try:
        cursor.execute("SELECT name, amount, category, date FROM expenses")
        rows = cursor.fetchall()
        expenses = [
            Expense(row[0], float(row[1]), row[2], row[3].strftime('%Y-%m-%d')) for row in rows
        ]
    except Exception as e:
        print(f"Error loading expenses: {e}")

# Save expenses to the PostgreSQL database
def save_expense(name, amount, category, date):
    try:
        cursor.execute(
            "INSERT INTO expenses (name, amount, category, date) VALUES (%s, %s, %s, %s)",
            (name, amount, category, date)
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving expense: {e}")

# Add a new expense
def add_expense(name, amount, category, date):
    global expenses
    category = Category.normalize(category)  # Normalize the category name
    amount = float(amount)  # Convert amount to float

    # Add new expense
    expenses.append(Expense(name, amount, category, date))
    save_expense(name, amount, category, date)

# Request handler
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            try:
                load_expenses()
                env = Environment(loader=FileSystemLoader('templates'))
                template = env.get_template('index.html')

                # Get filter values
                query_params = parse_qs(self.path[2:])
                filter_date = query_params.get('filter-date', [''])[0]
                filter_category = query_params.get('filter-category', [''])[0]

                filtered_expenses = expenses

                if filter_date:
                    filtered_expenses = [
                        exp for exp in filtered_expenses
                        if exp.date == filter_date
                    ]

                if filter_category:
                    filtered_expenses = [
                        exp for exp in filtered_expenses
                        if exp.category == filter_category
                    ]

                total_expenses = sum(expense.amount for expense in filtered_expenses)
                output = template.render(
                    expenses=filtered_expenses,
                    total_expenses=total_expenses,
                    categories=categories,
                    selected_category=filter_category,
                    selected_date=filter_date
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

    def serve_static_file(self):
        static_file_path = unquote(self.path[1:])
        full_path = os.path.join(os.getcwd(), static_file_path)

        if os.path.isfile(full_path):
            mime_type, _ = mimetypes.guess_type(full_path)

            self.send_response(200)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            self.end_headers()
            with open(full_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            name = data.get('name', [''])[0]
            amount = data.get('amount', [''])[0]
            category = data.get('category', [''])[0]
            date = data.get('date', [''])[0]

            if name and amount and category and date:
                add_expense(name, amount, category, date)

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

# Main function to start the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
