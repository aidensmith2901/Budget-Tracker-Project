#!/usr/bin/env python3
import sqlite3


def createbudgetDim(conn):
    # Create date dimension table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgetDim (
        categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (categoryID) REFERENCES categoryDim(catID)
    )
    """)
    conn.commit()

def addBudgetEntry(conn, categoryID, year, month, amount):
    conn.execute("""
        INSERT INTO budgetDim (categoryID, year, month, amount)
        VALUES (?, ?, ?, ?)
    """, (categoryID, year, month, amount))
    conn.commit()

def editBudgetEntry(conn, budgetID, amount):
    conn.execute("""
        UPDATE budgetDim
        SET amount = ?
        WHERE categoryID = ?
    """, (amount, budgetID))
    conn.commit()

def deleteBudgetEntry(conn, budgetID):
    conn.execute("""
        DELETE FROM budgetDim
        WHERE categoryID = ?
    """, (budgetID,))
    conn.commit()

def copyLastMonthBudget(conn, year, month):
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    cur = conn.execute("""
        SELECT categoryID, amount FROM budgetDim
        WHERE year = ? AND month = ?
    """, (prev_year, prev_month))

    rows = cur.fetchall()
    for row in rows:
        categoryID, amount = row
        addBudgetEntry(conn, categoryID, year, month, amount)

def resetMonthBudget(conn, year, month):
    conn.execute("""
        DELETE FROM budgetDim
        WHERE year = ? AND month = ?
    """, (year, month))
    conn.commit()

def displayBudgetForMonth(conn, year, month):
    cur = conn.execute("""
        SELECT categoryID, amount FROM budgetDim
        WHERE year = ? AND month = ?
    """, (year, month))

    rows = cur.fetchall()
    for row in rows:
        categoryID, amount = row
        print(f"Category ID: {categoryID}, Amount: {amount}")

def commitChanges(conn):
    conn.commit()

