#!/usr/bin/env python3
import sqlite3
from datetime import date, datetime, timedelta

def createDateDimTable(conn):
    # Create date dimension table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dateDim (
        date_id INTEGER PRIMARY KEY,
        date TEXT NOT NULL UNIQUE,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL
    )
    """)
    conn.commit()

def insertDate(conn, dt):
    date_str = dt.strftime("%Y-%m-%d")
    date_id = int(dt.strftime("%Y%m%d"))
    conn.execute("""
        INSERT OR IGNORE INTO dateDim (date_id, date, year, month, day)
        VALUES (?, ?, ?, ?, ?)
    """, (date_id, date_str, dt.year, dt.month, dt.day))

def addToDateDim(conn, startDate, endDate):
    current = startDate
    while current <= endDate:
        insertDate(conn, current)
        current += timedelta(days=1)
    conn.commit()

def checkDateDimDates(conn):
    cur = conn.execute("SELECT MAX(date_id) FROM dateDim")
    row = cur.fetchone()
    latestID = row[0]
    if latestID is None:
        return None
    return datetime.strptime(str(latestID), "%Y%m%d").date()

def initializeDateDim(conn):
    startDate = date(1950, 1, 1)
    today = datetime.today().date()
    oneYearOut = today + timedelta(days=365)
    addToDateDim(conn, startDate, oneYearOut)

def updateDateDim(conn):
    today = datetime.today().date()
    endDate = today + timedelta(days=365)
    latestDate = checkDateDimDates(conn)
    if latestDate is None:
        initializeDateDim(conn)
        return
    if latestDate < endDate:
        addToDateDim(conn, latestDate + timedelta(days=1), endDate)