import os
import psycopg2

# Set up the connection to the database using the DATABASE_URL environment variable
DATABASE_URL = os.environ['DATABASE_URL']

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    # Create the investors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            amount_invested REAL NOT NULL,
            promised_return REAL NOT NULL,
            package VARCHAR(100) NOT NULL,
            duration INTEGER NOT NULL,
            daily_income REAL NOT NULL,
            investment_date TIMESTAMP NOT NULL
        )
    ''')

    # Commit the changes to the database
    connection.commit()

    print("Database schema created successfully!")

except Exception as e:
    print("Error creating the database schema:", e)

finally:
    # Close the connection
    cursor.close()
    connection.close()
