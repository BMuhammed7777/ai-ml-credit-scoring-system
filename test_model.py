# test_model.py
import joblib
import sys

try:
    print("Loading model...")
    model = joblib.load('models/credit_scoring_model.pkl')
    print(f"✅ Model loaded: {type(model)}")
    print(f"Model type: {model.__class__.__name__}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)