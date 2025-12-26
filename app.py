# app.py (FULL UPDATED VERSION)
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import sys
import os

# Database functions import
from database import init_database, save_application, get_all_applications, get_statistics

app = Flask(__name__)

# Initialize database
init_database()

# Load models with error handling
print("=" * 50)
print("Loading ML models...")
print("=" * 50)

try:
    # Check if model files exist
    model_path = 'models/credit_scoring_model.pkl'
    encoder_path = 'models/credit_score_encoder.pkl'
    cat_encoder_path = 'models/cat_encoders.pkl'

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Load model
    model = joblib.load(model_path)
    print(f"✅ Model loaded: {type(model).__name__}")

    # Load label encoder
    label_encoder = joblib.load(encoder_path)
    print(f"✅ Label encoder loaded")

    # Load categorical encoders
    cat_encoders = joblib.load(cat_encoder_path)
    print(f"✅ Categorical encoders loaded")

    print("=" * 50)
    print("✅ ALL MODELS LOADED SUCCESSFULLY!")
    print("=" * 50)

except ModuleNotFoundError as e:
    print(f"\n❌ ERROR: Missing Python package!")
    print(f"Error: {e}")
    print("\n💡 SOLUTION: Install the missing package:")
    print("   pip install xgboost")
    sys.exit(1)

except FileNotFoundError as e:
    print(f"\n❌ ERROR: Model files not found!")
    print(f"Error: {e}")
    print("\n💡 SOLUTION: Make sure model files are in 'models/' folder:")
    print("   - credit_scoring_model.pkl")
    print("   - credit_score_encoder.pkl")
    print("   - cat_encoders.pkl")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ ERROR: Could not load models!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    sys.exit(1)

# Credit score mapping
SCORE_MAPPING = {
    0: {'name': 'Poor', 'min': 300, 'max': 579, 'color': 'red'},
    1: {'name': 'Standard', 'min': 580, 'max': 669, 'color': 'orange'},
    2: {'name': 'Good', 'min': 670, 'max': 850, 'color': 'green'}
}


def calculate_credit_score(prediction, probability):
    """Calculate numeric credit score from prediction"""
    category = SCORE_MAPPING[prediction]
    score_range = category['max'] - category['min']
    confidence = probability[prediction]
    credit_score = int(category['min'] + (score_range * confidence))
    return credit_score, category['name'], category['color']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        name = request.form.get('name')
        age = int(request.form.get('age'))
        occupation = int(request.form.get('occupation', 0))
        annual_income = float(request.form.get('annual_income'))
        monthly_salary = float(request.form.get('monthly_salary'))
        num_bank_accounts = int(request.form.get('num_bank_accounts'))
        num_credit_card = int(request.form.get('num_credit_card'))
        interest_rate = int(request.form.get('interest_rate', 10))
        num_of_loan = int(request.form.get('num_of_loan', 0))
        delay_from_due_date = int(request.form.get('delay_from_due_date', 0))
        num_delayed_payment = int(request.form.get('num_delayed_payment', 0))
        outstanding_debt = float(request.form.get('outstanding_debt', 0))
        credit_utilization_ratio = float(request.form.get('credit_utilization_ratio', 0))
        credit_history_age = int(request.form.get('credit_history_age', 0))
        total_emi_per_month = float(request.form.get('total_emi_per_month', 0))
        monthly_balance = float(request.form.get('monthly_balance', 0))

        # Feature engineering
        debt_ratio = outstanding_debt / annual_income if annual_income > 0 else 0
        emi_ratio = total_emi_per_month / monthly_salary if monthly_salary > 0 else 0
        inquiry_per_account = 0

        # Create features array (26 features - match training data)
        features = pd.DataFrame([[
            1,  # Month
            age,
            occupation,
            annual_income,
            monthly_salary,
            num_bank_accounts,
            num_credit_card,
            interest_rate,
            num_of_loan,
            0,  # Type_of_Loan
            delay_from_due_date,
            num_delayed_payment,
            0,  # Changed_Credit_Limit
            0,  # Num_Credit_Inquiries
            1,  # Credit_Mix (Good=1)
            outstanding_debt,
            credit_utilization_ratio,
            credit_history_age,
            1,  # Payment_of_Min_Amount (Yes=1)
            total_emi_per_month,
            0,  # Amount_invested_monthly
            0,  # Payment_Behaviour
            monthly_balance,
            debt_ratio,
            emi_ratio,
            inquiry_per_account
        ]], columns=[
            'Month', 'Age', 'Occupation', 'Annual_Income', 'Monthly_Inhand_Salary',
            'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan',
            'Type_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment',
            'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Credit_Mix',
            'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
            'Payment_of_Min_Amount', 'Total_EMI_per_month', 'Amount_invested_monthly',
            'Payment_Behaviour', 'Monthly_Balance', 'Debt_Ratio', 'EMI_Ratio',
            'Inquiry_per_Account'
        ])

        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        # Calculate credit score
        credit_score, category, color = calculate_credit_score(prediction, probability)

        # Decision logic
        if credit_score >= 670:
            decision = "Approved"
            risk = "Low Risk"
        elif credit_score >= 580:
            decision = "Review Required"
            risk = "Medium Risk"
        else:
            decision = "Rejected"
            risk = "High Risk"

        # Save to database
        application_data = {
            'name': name,
            'age': age,
            'occupation': occupation,
            'annual_income': annual_income,
            'monthly_salary': monthly_salary,
            'num_bank_accounts': num_bank_accounts,
            'num_credit_card': num_credit_card,
            'interest_rate': interest_rate,
            'num_of_loan': num_of_loan,
            'delay_from_due_date': delay_from_due_date,
            'num_delayed_payment': num_delayed_payment,
            'outstanding_debt': outstanding_debt,
            'credit_utilization_ratio': credit_utilization_ratio,
            'credit_history_age': credit_history_age,
            'total_emi_per_month': total_emi_per_month,
            'monthly_balance': monthly_balance,
            'credit_score': credit_score,
            'credit_category': category,
            'decision': decision,
            'prediction_probability': float(max(probability))
        }

        save_application(application_data)

        return render_template('result.html',
                               name=name,
                               credit_score=credit_score,
                               category=category,
                               risk=risk,
                               decision=decision,
                               confidence=round(max(probability) * 100, 2),
                               color=color)

    except Exception as e:
        error_msg = f"Prediction error: {str(e)}"
        print(f"❌ {error_msg}")
        return render_template('error.html', error=error_msg), 400


@app.route('/admin')
def admin():
    try:
        stats = get_statistics()
        return render_template('admin.html', stats=stats)
    except Exception as e:
        return f"Admin dashboard error: {str(e)}", 500


@app.route('/api/stats')
def api_stats():
    """API endpoint for Grafana"""
    try:
        stats = get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 Starting Flask application...")
    print("🌐 Open browser: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)