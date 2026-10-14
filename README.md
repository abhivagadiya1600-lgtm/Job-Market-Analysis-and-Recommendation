# Job Market Analysis & Recommendation System
## Project Overview

This project analyzes job-market data and provides job recommendations based on user skills.

The system includes:

- Job market analysis
- Job demand analysis
- Compensation analysis
- High-demand job prediction
- Country-wise hourly-rate analysis
- Job recommendation engine
- REST API
- Interactive Streamlit dashboard

---

# Job Recommendation API
The project provides a FastAPI-based REST API for recommending jobs based on user skills.

## Base URL
```text
http://127.0.0.1:8000

## Project Analysis and Forecasting

### Features
- Job market data preprocessing and cleaning
- Job-title keyword and hourly-rate analysis
- Emerging job category analysis
- High-demand job role analysis and forecasting
- Country-wise hourly-rate comparison
- Monthly job posting trend analysis
- Remote-work keyword analysis
- Future job-demand forecast
- Skill-based job recommendation dashboard
- Interactive filters and job application links

### Technologies Used
- Python
- Pandas and NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- Flask or FastAPI (if used by the API)

### Analysis Outputs
Generated reports and charts are saved in `analysis_output/`.

Key files:
- `keyword_compensation_analysis.csv`
- `emerging_job_categories.csv`
- `high_demand_job_roles.csv`
- `country_average_hourly_rate.csv`
- `monthly_job_demand.csv`
- `future_job_demand_forecast.csv`
- `future_trend_summary.csv`
- `future_job_market_trend.png`

### How to Run

1. Activate the project's virtual environment.
2. Install dependencies:
`pip install -r requirements.txt`
3. Run data analysis:
`python src/analysis.py`
4. Start the recommendation dashboard:
`python -m streamlit run app.py`

Live Demo
Dashboard: https://job-market-dashboard-q3st.onrender.com
API Documentation: https://job-market-api-otow.onrender.com/docs

Key Dashboard Metrics
Total job listings: 244,828
Countries covered: 212
Hourly job listings: 140,937

Technology Stack
Python, Pandas, NumPy
Matplotlib and Streamlit
FastAPI
Docker and Render
Git and GitHub

Project Objective
Analyze global job-market trends, identify in-demand roles, compare hourly job rates, and recommend job opportunities based on users’ skills.

Author
Abhishek Vagadiya
Aspiring Data Analyst | Python | SQL | Power BI | Excel

GitHub: https://github.com/abhivagadiya1600-lgtm
