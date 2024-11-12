from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Function to initialize the database
def init_db():
    """
    This function initializes the SQLite database by creating a table for investors.
    If the database does not exist, it will be created.
    The table includes fields for id, name, amount invested, promised return, package type, duration, and daily income.
    """
    if not os.path.exists('ponzi.db'):
        conn = sqlite3.connect('ponzi.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount_invested REAL NOT NULL,
                promised_return REAL NOT NULL,
                package TEXT NOT NULL,
                duration INTEGER NOT NULL,
                daily_income REAL NOT NULL,
                investment_date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Define route to the home page
@app.route('/')
def index():
    """
    Home page route that displays all current investors and the total amount invested.
    Connects to the database to fetch all investor data and passes it to the HTML template for rendering.
    """
    conn = sqlite3.connect('ponzi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investors")
    investors = cursor.fetchall()
    total_invested = sum([investor[2] for investor in investors])
    conn.close()
    return render_template('index.html', investors=investors, total_invested=total_invested)

# Define route to the investment packages page
@app.route('/packages')
def packages():
    """
    Displays the different investment packages available.
    The packages are hard-coded but can be dynamically generated if needed.
    """
    return render_template('packages.html')

# Define route to handle new investments
@app.route('/invest', methods=['GET', 'POST'])
def invest():
    """
    Handles both GET and POST requests for the invest page.
    If it's a GET request, it simply displays the investment form.
    If it's a POST request, it processes the submitted data, stores it in the database, and redirects to the home page.
    """
    if request.method == 'POST':
        # Retrieve data from the form submission
        name = request.form['name']
        amount = float(request.form['amount'])
        package = request.form['package']
        investment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine the investment details based on the selected package
        if package == 'Super Partner':
            promised_return = amount * 1.15  # Example of 15% return
            duration = 1095  # Duration in days (3 years)
            daily_income = 0
        elif package == 'VIP7':
            promised_return = amount * 1.1  # Example of 10% return
            duration = 1095
            daily_income = 164.4
        elif package == 'VIP6':
            promised_return = amount * 1.05  # Example of 5% return
            duration = 1095
            daily_income = 72.0
        elif package == 'VIP5':
            promised_return = amount * 1.08  # 8% return
            duration = 1095
            daily_income = 34.8
        elif package == 'VIP4':
            promised_return = amount * 1.07  # 7% return
            duration = 1095
            daily_income = 16.56
        elif package == 'VIP3':
            promised_return = amount * 1.04  # 4% return
            duration = 1095
            daily_income = 5.04
        elif package == 'VIP2':
            promised_return = amount * 1.03  # 3% return
            duration = 1095
            daily_income = 1.44
        elif package == 'Free Equipment':
            promised_return = 0
            duration = 2  # Short duration for free equipment
            daily_income = 1.92
        else:
            promised_return = amount * 1.15  # Default return
            duration = 1095
            daily_income = 0

        # Insert the investor's data into the database
        conn = sqlite3.connect('ponzi.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO investors (name, amount_invested, promised_return, package, duration, daily_income, investment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, amount, promised_return, package, duration, daily_income, investment_date))
        conn.commit()
        conn.close()

        # Redirect the user to the home page to display updated investor information
        return redirect(url_for('index'))
    return render_template('invest.html')

# Define route for user profile (if needed)
@app.route('/profile/<int:investor_id>')
def profile(investor_id):
    """
    Displays individual investor's profile.
    Fetches investor data from the database based on the provided investor ID.
    """
    conn = sqlite3.connect('ponzi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investors WHERE id = ?", (investor_id,))
    investor = cursor.fetchone()
    conn.close()
    return render_template('profile.html', investor=investor)

# Main block to run the application
if __name__ == '__main__':
    """
    Initializes the database and runs the Flask server in debug mode.
    """
    init_db()
    app.run(debug=True)