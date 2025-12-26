\# AI/ML Powered Credit Scoring System



\*\*University Software Engineering Final Project\*\*



This project is a complete credit scoring system built using Machine Learning techniques, a Flask backend, SQLite database, simple HTML frontend, and Grafana for admin dashboard visualization.



\## Project Overview



The goal of this system is to predict credit risk for loan applicants using machine learning models. User inputs are processed with feature engineering, scored by a trained ML model, and results are displayed on a web interface. An admin dashboard provides insights into data and model performance using Grafana.



The project fully satisfies the instructor's requirements:

\- Simple HTML frontend

\- Flask backend

\- SQLite3 database

\- Feature engineering

\- Machine Learning model for credit scoring

\- Data visualization

\- Grafana admin dashboard

\- Full web deployment



\## Features



\- \*\*User Interface\*\*: Simple and clean HTML forms for loan application input and result display.

\- \*\*Backend\*\*: Flask web framework for handling requests, processing data, and serving predictions.

\- \*\*Database\*\*: SQLite3 for storing application data and historical records.

\- \*\*Machine Learning\*\*:

&nbsp; - Feature engineering (handling categorical variables, scaling, etc.)

&nbsp; - Trained models saved as `.pkl` files (e.g., category encoders and scoring model)

&nbsp; - Credit risk prediction with probability scores

\- \*\*Visualization\*\*: Plots and charts generated for results and data exploration.

\- \*\*Admin Dashboard\*\*: Grafana integration for monitoring data, model performance, and system metrics.



\## Technologies Used



\- Python (Flask)

\- SQLite3

\- Scikit-learn / Pandas / NumPy for ML and data processing

\- HTML/CSS for frontend

\- Matplotlib / Plotly for visualizations

\- Grafana for admin dashboard

\- Pickle for model persistence



\## Setup and Running the Project



1\. Clone the repository:

&nbsp;  ```bash

&nbsp;  git clone https://github.com/BMuhammed7777/ai-ml-credit-scoring-system.git

&nbsp;  cd ai-ml-credit-scoring-system

2\. Install dependencies:

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

3\. Run the Flask application:

&nbsp;  ```bash

&nbsp;  python app.py

4\. Open your browser and go to http://127.0.0.1:5000

5\. For Grafana dashboard:

Start Grafana (Docker or local installation required)

Import the provided dashboard configuration (if available) or connect to the SQLite data source



Project Structure:

.

├── app.py                  # Flask main application

├── database.py             # Database operations

├── test\_model.py           # Model testing script

├── requirements.txt        # Python dependencies

├── data/

│   └── credit\_system.db    # SQLite database (pre-populated with sample data)

├── models/

│   ├── cat\_encoders.pkl

│   ├── credit\_score\_encoder.pkl

│   └── credit\_scoring\_model.pkl  # Trained ML models

├── templates/

│   ├── index.html          # Main page

│   ├── admin.html          # Admin view

│   └── result.html         # Prediction result page

└── README.md



Notes



The trained ML models are included in the models/ folder.

Database is pre-populated with sample data for testing.

Grafana dashboard configuration can be extended based on requirements.



Thank you for reviewing the project!

Author: Muhammed Bayramov

Course: Software Engineering

Date: December 2025

