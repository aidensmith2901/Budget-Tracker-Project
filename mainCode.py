#!/usr/bin/env python3
import sqlite3
import datetime
import dateDimCode
import categoryDim
import cliCategory

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect("./data/budget_tracker.db")
cursor = conn.cursor()

def main():
    # Connect to DB
    conn = sqlite3.connect("./data/budget_tracker.db")

    # Create table
    dateDimCode.createDateDimTable(conn)

    # Initialize or update dateDim
    dateDimCode.updateDateDim(conn)
    categoryDim.populateCategoryDim(conn)

    cliCategory.categoryCLI(conn)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()



# def startUpRoutine(conn):
#     createTables(conn)
#     dateDimCode.refresh_date_dim(conn)
    
# def createTables(conn):
#     # Create transaction fact table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transFact (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         amount REAL NOT NULL,
#         category TEXT NOT NULL,
#         description TEXT,
#         date_id INTEGER NOT NULL,
#         FOREIGN KEY (date_id) REFERENCES dateDim(date_id)
#     )
#     """)
#     dateDimCode.createDateDimTable(conn)

# def buildDateTable(dateStr):
#     # dtDate = checkDate(dateStr)
#     # if dtDate is None:   # quit early if invalid
#     #     return None    
#     # year, month, day, date, dateInt = parseDate(dateStr)
#     startDate = datetime.date(1950, 1, 1)
#     endDate = datetime.date.today() + datetime.timedelta(days=365)

# def checkDate(dateStr):
#     formats = ["%d-%m-%Y", "%d/%m/%Y"]
#     for fmt in formats:
#         try:
#             return datetime.strptime(dateStr, fmt)  # return dt object if valid
#         except ValueError:
#             continue
#     return None  # invalid date

# # def parseDate(dtDate):
#     year = dtDate.year
#     month = dtDate.month
#     day = dtDate.day
#     date = dtDate.strftime("%Y-%m-%d")       # normalized ISO string
#     dateInt = int(dtDate.strftime("%Y%m%d")) # YYYYMMDD integer
#     return year, month, day, date, dateInt

# def add_transaction(amount, category, description="", trans_date=None):
#     """
#     Add a transaction to the SQLite database.
    
#     Parameters:
#         amount (float): Positive for income, negative for expense.
#         category (str): Category of the transaction (e.g., 'Food', 'Rent').
#         description (str): Optional description.
#         trans_date (str): Date in 'YYYY-MM-DD'. Defaults to today.
#     """
#     if trans_date is None:
#         error="No date is entered"
    
#     cursor.execute("""
#     INSERT INTO transactions (amount, category, description, date)
#     VALUES (?, ?, ?, ?)
#     """, (amount, category, description, trans_date))
#     conn.commit()


# def get_transactions(category=None):
#     """
#     Retrieve transactions from the database.
#     Optionally filter by category.
#     """
#     if category:
#         cursor.execute("SELECT * FROM transactions WHERE category = ?", (category,))
#     else:
#         cursor.execute("SELECT * FROM transactions")
#     return cursor.fetchall()

# # Example usage:
# add_transaction(-50.75, "Food", "Groceries at Walmart")
# add_transaction(2000, "Salary", "Monthly paycheck", "2026-01-07")

# print(get_transactions())          # All transactions
# print(get_transactions("Food"))    # Only Food transactions