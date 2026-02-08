#!/usr/bin/env python3
import sqlite3

def createCategoryDim(conn):
    # Create date dimension table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoryDim (
        catID INTEGER PRIMARY KEY AUTOINCREMENT,
        catName TEXT NOT NULL UNIQUE,
        parentCat INTEGER,
        isActive INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (parentCat) REFERENCES categoryDim(catID)
    )
    """)
    conn.commit()

def populateCategoryDim(conn):
    cursor = conn.cursor()
    createCategoryDim(conn)
    cursor.execute("SELECT COUNT(*) FROM categoryDim")
    count = cursor.fetchone()[0]
    if count > 0:
        return  # Already populated, nothing to do
    DEFAULT_CATEGORIES = {
        "Housing": [
            "Rent", "Mortgage", "Property Taxes", "Home Insurance",
            "Home Maintenance", "HOA Fees", "Electricity", "Water",
            "Gas Utility", "Internet", "Trash & Recycling"
        ],
        "Food": [
            "Groceries", "Restaurants", "Fast Food", "Coffee Shops",
            "Bars & Alcohol", "Meal Delivery"
        ],
        "Transportation": [
            "Gas", "Parking", "Public Transit", "Rideshare",
            "Car Payment", "Car Insurance", "Car Maintenance",
            "Car Registration"
        ],
        "Pets": [
            "Dog Food", "Cat Food", "Treats", "Toys",
            "Vet Visits", "Grooming", "Pet Insurance"
        ],
        "Personal Care": [
            "Haircuts", "Toiletries", "Skincare", "Gym Membership",
            "Vitamins & Supplements"
        ],
        "Entertainment": ["Movies", "Concerts", "Sporting Events", 
            "Hobbies", "Subscriptions"
        ],
        "Shopping": [
            "Clothing", "Shoes", "Electronics", "Home Goods",
            "Gifts"
        ],
        "Work & Education": [
            "Work Supplies", "Professional Fees", "Courses",
            "Books", "Tuition"
        ],
        "Health": [
            "Health Insurance", "Doctor Visits", "Dentist",
            "Prescriptions", "Therapy", "Medical Devices"
        ],
        "Debt Payments": [
            "Credit Card Payment", "Student Loan Payment",
            "Personal Loan Payment"
        ],
        "Savings": [
            "Emergency Fund", "Retirement", "Investments",
            "Big Purchases Fund"
        ],
        "Taxes": [
            "Federal Taxes", "State Taxes", "Estimated Taxes",
            "Accountant Fees"
        ],
        "Travel": [
            "Flights", "Hotels", "Rental Cars", "Travel Food",
            "Activities", "Travel Insurance"
        ],
        "Income": [
            "Salary","Bonus","Overtime","Tips","Freelance / Contract Work",
            "Business Income","Investment Income","Rental Income",
            "Refunds & Reimbursements","Other Income"
        ]
    }
    for parentName, children in DEFAULT_CATEGORIES.items():
        # Insert parent
        cursor.execute("""
            INSERT INTO categoryDim (catName, parentCat)
            VALUES (?, NULL)
        """, (parentName,))
        parentID = cursor.lastrowid
        # Insert children
        for childName in children:
            cursor.execute("""
                INSERT INTO categoryDim (catName, parentCat)
                VALUES (?, ?)
            """, (childName, parentID))
    conn.commit()

def addCategory(conn, catName, parentCat=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO categoryDim (catName, parentCat)
        VALUES (?, ?)
    """, (catName, parentCat))
    if categoryExists(conn, catName):
        return False
    conn.commit()

def editCategory(conn, catID, newName=None, newParentCat=None, isActive=None):
    cursor = conn.cursor()
    updates = []
    params = []

    if newName is not None:
        updates.append("catName = ?")
        params.append(newName)
    if newParentCat is not None:
        updates.append("parentCat = ?")
        params.append(newParentCat)
    if isActive is not None:
        updates.append("isActive = ?")
        params.append(isActive)
    if not updates:
        return

    params.append(catID)
    sql = f"UPDATE categoryDim SET {', '.join(updates)} WHERE catID = ?"
    cursor.execute(sql, params)
    conn.commit()

def deleteCategory(conn, catID):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categoryDim
        SET isActive = 0
        WHERE catID = ?
    """, (catID,))
    conn.commit()

def getParentCategories(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT catID, catName
        FROM categoryDim
        WHERE parentCat IS NULL AND isActive = 1
        ORDER BY catName
    """)
    return cursor.fetchall()

def getChildCategories(conn, parentCat):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT catID, catName
        FROM categoryDim
        WHERE parentCat = ? AND isActive = 1
        ORDER BY catName
    """, (parentCat,))
    return cursor.fetchall()

def categoryExists(conn, catName):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM categoryDim
        WHERE LOWER(catName) = LOWER(?) AND isActive = 1
    """, (catName,))
    return cursor.fetchone() is not None

