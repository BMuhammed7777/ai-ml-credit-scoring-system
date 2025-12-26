# database.py
import sqlite3
import pandas as pd
from datetime import datetime


def init_database():
    """Database və table-ları yarat"""
    conn = sqlite3.connect('data/credit_system.db')
    cursor = conn.cursor()

    # Applications table - user müraciətləri
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            occupation INTEGER,
            annual_income REAL,
            monthly_salary REAL,
            num_bank_accounts INTEGER,
            num_credit_card INTEGER,
            interest_rate INTEGER,
            num_of_loan INTEGER,
            delay_from_due_date INTEGER,
            num_delayed_payment INTEGER,
            outstanding_debt REAL,
            credit_utilization_ratio REAL,
            credit_history_age INTEGER,
            total_emi_per_month REAL,
            monthly_balance REAL,

            credit_score INTEGER,
            credit_category TEXT,
            decision TEXT,
            prediction_probability REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            total_applications INTEGER,
            approved INTEGER,
            rejected INTEGER,
            avg_credit_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


def save_application(data):
    """Yeni müraciəti saxla"""
    conn = sqlite3.connect('data/credit_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO applications (
            name, age, occupation, annual_income, monthly_salary,
            num_bank_accounts, num_credit_card, interest_rate,
            num_of_loan, delay_from_due_date, num_delayed_payment,
            outstanding_debt, credit_utilization_ratio, 
            credit_history_age, total_emi_per_month, monthly_balance,
            credit_score, credit_category, decision, prediction_probability
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['age'], data['occupation'],
        data['annual_income'], data['monthly_salary'],
        data['num_bank_accounts'], data['num_credit_card'],
        data['interest_rate'], data['num_of_loan'],
        data['delay_from_due_date'], data['num_delayed_payment'],
        data['outstanding_debt'], data['credit_utilization_ratio'],
        data['credit_history_age'], data['total_emi_per_month'],
        data['monthly_balance'], data['credit_score'],
        data['credit_category'], data['decision'],
        data['prediction_probability']
    ))

    conn.commit()
    conn.close()
    print("✅ Application saved to database!")


def get_all_applications():
    """Bütün müraciətləri əldə et"""
    conn = sqlite3.connect('data/credit_system.db')
    df = pd.read_sql_query(
        "SELECT * FROM applications ORDER BY created_at DESC LIMIT 100",
        conn
    )
    conn.close()
    return df


def get_statistics():
    """Admin dashboard üçün statistikalar"""
    conn = sqlite3.connect('data/credit_system.db')

    stats = {}

    # Total applications
    stats['total'] = pd.read_sql_query(
        "SELECT COUNT(*) as count FROM applications", conn
    ).iloc[0]['count']

    # Approved/Rejected
    stats['approved'] = pd.read_sql_query(
        "SELECT COUNT(*) as count FROM applications WHERE decision='Approved'", conn
    ).iloc[0]['count']

    stats['rejected'] = pd.read_sql_query(
        "SELECT COUNT(*) as count FROM applications WHERE decision='Rejected'", conn
    ).iloc[0]['count']

    # Average credit score
    avg_score = pd.read_sql_query(
        "SELECT AVG(credit_score) as avg FROM applications", conn
    ).iloc[0]['avg']
    stats['avg_score'] = round(avg_score, 2) if avg_score else 0

    # By category
    stats['by_category'] = pd.read_sql_query(
        "SELECT credit_category, COUNT(*) as count FROM applications GROUP BY credit_category",
        conn
    ).to_dict('records')

    # Recent applications
    stats['recent'] = pd.read_sql_query(
        "SELECT name, credit_score, decision, created_at FROM applications ORDER BY created_at DESC LIMIT 10",
        conn
    ).to_dict('records')

    conn.close()
    return stats


if __name__ == '__main__':
    init_database()