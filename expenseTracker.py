import mysql.connector
from pymongo import MongoClient
from datetime import datetime

# ---------- MongoDB Setup ----------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ExpenseDB"]
mongo_collection = mongo_db["expenses"]

# ---------- MySQL Setup ----------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="shruti",         
    password="shruti123", 
    database="ExpenseDB"
)
mysql_cursor = mysql_conn.cursor()

# ---------- Add Expense ----------
def add_expense():
    amount = float(input("Enter amount ₹: "))
    category = input("Enter category: ")
    note = input("Note (optional): ")
    date = datetime.now()

    # Insert into MySQL
    mysql_query = "INSERT INTO expenses (amount, category, note, date) VALUES (%s, %s, %s, %s)"
    mysql_cursor.execute(mysql_query, (amount, category, note, date))
    mysql_conn.commit()

    # Insert into MongoDB
    mongo_collection.insert_one({
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    })

    print("✅ Expense added to both MySQL & MongoDB.")

# ---------- View Expenses ----------
def view_expenses():
    print("\n MySQL Expenses:")
    mysql_cursor.execute("SELECT * FROM expenses")
    for row in mysql_cursor.fetchall():
        print(f"₹{row[1]} | {row[2]} | {row[3]} | {row[4].strftime('%d-%m-%Y')}")

    print("\n MongoDB Expenses:")
    for doc in mongo_collection.find():
        print(f"₹{doc['amount']} | {doc['category']} | {doc.get('note', '')} | {doc['date'].strftime('%d-%m-%Y')}")

# ---------- Main Menu ----------
def main():
    while True:
        print("\n..... SMART EXPENSE TRACKER .....")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Choose: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("👋 Bye, You’re now financially aware!")
            break
        else:
            print("Try again.")

if __name__ == "__main__":
    main()