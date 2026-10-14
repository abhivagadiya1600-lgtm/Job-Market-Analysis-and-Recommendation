import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from src.recommendation import get_recommendations

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Job Market Analysis & Recommendation",
    page_icon="💼",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #ffffff;
} 

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

h1 {
    color: #17365D;
    font-weight: 700;
}

h2, h3 {
    color: #17365D;
}

.metric-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.title("💼 Job Market Analysis & Recommendation")

st.write(
    "Analyze job-market trends and find jobs based on your skills."
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    possible_files = [
        "jobs.csv",
        "job_data.csv",
        "job_market.csv",
        "jobs_data.csv",
        "data.csv"
    
        "data/jobs.csv",
        "data/job_data.csv",
        "data/job_market.csv",
        "data/jobs_data.csv",
        "data/data.csv"
    ]
# Check all known locations

    for file_path in possible_files:

        if os.path.exists(file_path):

            try:

                if file_path.lower().endswith(".csv"):

                    data = pd.read_csv(file_path)

                elif file_path.lower().endswith((".xlsx", ".xls")):

                    data = pd.read_excel(file_path)

                else:

                    continue

                st.success(f"Dataset loaded successfully: {file_path}")

                return data

            except Exception as e:

                st.error(

                    f"Error reading dataset '{file_path}': {e}"

                )

                return None

    # Automatically search the data folder

    if os.path.exists("data"):
        for file_name in os.listdir("data"):
            file_path = os.path.join(
                "data",
                file_name
            )

            if file_name.lower().endswith(".csv"):
                try:
                    data = pd.read_csv(file_path)
                    st.success(
                        f"Dataset loaded successfully: {file_path}"
                    )

                    return data

                except Exception as e:

                    st.error(
                        f"Error reading {file_path}: {e}"
                    )

                    return None

            elif file_name.lower().endswith(
                (".xlsx", ".xls")
            ):

                try:

                    data = pd.read_excel(file_path)

                    st.success(
                        f"Dataset loaded successfully: {file_path}"
                    )
                    return data

                except Exception as e:

                    st.error(
                        f"Error reading {file_path}: {e}"
                    )

                    return None
    return None


df = load_data()


# ============================================================
# IF DATASET NOT FOUND
# ============================================================

if df is None:

    st.error(
        "Dataset not found. Please keep your CSV/Excel file in the same "
        "folder as app.py."
    )

    st.info(
        "Supported filenames: jobs.csv, job_data.csv, job_market.csv, "
        "jobs_data.csv or data.csv"
    )

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)


# ============================================================
# DEBUG
# ============================================================


# Uncomment this if you want to see your actual columns
# st.write("Columns:", df.columns.tolist())


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    # Try partial matching
    for col in df.columns:

        for name in possible_names:

            if name in col:
                return col

    return None


# ============================================================
# FIND IMPORTANT COLUMNS AUTOMATICALLY
# ============================================================

country_col = find_column([
    "country",
    "countries",
    "location_country",
    "job_country",
    "country_name"
])

rate_col = find_column([
    "hourly_rate",
    "hourlyrate",
    "hourly_rate_usd", 
    "rate_per_hour",
    "hourly",
    "salary_per_hour",
    "hourly_salary",
    "budget"
])

job_title_col = find_column([
   "job_title",
   "jobtitle",
   "title",
   "job_name",
   "position"
])

job_type_col = find_column([
   "job_type",
   "jobtype",
   "employment_type",
   "type"
])

description_col = find_column([
   "description",
   "job_description",
   "details"
])


# ============================================================
# COUNTRY CLEANING
# ============================================================

if country_col is not None:

    df[country_col] = (
        df[country_col]
        .astype("string")
        .str.strip()
    )

    # Remove invalid values
    invalid_country_values = [
        "",
        "nan",
        "none", 
        "null",
        "unknown",
        "n/a",
        "na"
    ]

    valid_country = df[
        df[country_col].notna() 
        & ~df[country_col].str.lower().isin(invalid_country_values)
    ]

    country_count = valid_country[country_col].nunique()

else:

    country_count = 0


# ============================================================
# TOTAL JOBS
# ============================================================

total_jobs = len(df)


# ============================================================
# HOURLY JOBS
# ============================================================

# HOURLY JOBS
if "is_hourly" in df.columns:
    hourly_jobs = (
        df["is_hourly"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
        .sum()
    )

else:
    hourly_jobs = 0


# ============================================================
# HOURLY RATE CLEANING
# ============================================================

avg_hourly_rate = 0.0

if rate_col is not None:
    rate_series = df[rate_col].copy()
    rate_series = rate_series.astype("string")
    rate_series = (
        rate_series
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("USD", "", regex=False)
        .str.replace("usd", "", regex=False)
        .str.strip()
    )
    

    rate_series = rate_series.str.extract(
        r"(\d+(?:\.\d+)?)",
        expand=False
    )

    rate_series = pd.to_numeric(
        rate_series,
        errors="coerce"
    )


# ============================================================
# AVERAGE JOB BUDGET
# ============================================================

avg_job_budget = 0.0

if rate_col is not None:

    budget_values = df[rate_col].astype("string")

    budget_values = (
        budget_values
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
    )

    budget_values = pd.to_numeric(
        budget_values,
        errors="coerce"
    )

    valid_budgets = budget_values.dropna()

    if not valid_budgets.empty:
        avg_job_budget = valid_budgets.mean()

if pd.isna(avg_job_budget):
    avg_job_budget = 0.0

# Safety check

if pd.isna(avg_hourly_rate):
    avg_hourly_rate = 0.0


# ============================================================
# JOB MARKET OVERVIEW
# ============================================================

st.header("📊 Job Market Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Jobs",
        f"{total_jobs:,}"
    )


with col2:
    st.metric(
        "Countries",
        f"{country_count:,}"
    )


with col3:
    st.metric(
        "Hourly Jobs",
        f"{hourly_jobs:,}"
    )


with col4:
    st.metric(
        "Avg Job Budget",
        f"${avg_job_budget:,.2f}"
    )


# ============================================================
# JOB MARKET ANALYSIS
# ============================================================

st.header("🌍 Job Market Analysis")


# ============================================================
# TOP COUNTRIES BY NUMBER OF JOBS
# ============================================================

st.subheader("Top Countries by Number of Jobs")
if country_col is not None:
    country_data = (
        valid_country[country_col]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_data.columns = ["Country", "Jobs"]
    if not country_data.empty:
        st.bar_chart(
            country_data.set_index("Country")
        )

        st.dataframe(
            country_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("No valid country data found.")

else:
    st.warning("Country column was not detected in the dataset.")


# ============================================================
# TOP JOB TITLES
# ============================================================

st.subheader("💼 Top Job Titles")

if job_title_col is not None:

    title_data = (
        df[job_title_col]
        .astype(str)
        .str.strip()
    )

    title_data = title_data[
        ~title_data.str.lower().isin([
            "",
            "nan",
            "none",
            "null"
        ])
    ]

    top_titles = (
        title_data
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_titles.columns = [
        "Job Title",
        "Jobs"
    ]

    if not top_titles.empty:
        st.bar_chart(
            top_titles.set_index("Job Title")
        )

        st.dataframe(
            top_titles,
            use_container_width=True,
            hide_index=True
        )

else:

    st.warning(
        "Job title column was not detected."
    )


# ============================================================
# JOB TYPE ANALYSIS
# ============================================================

st.subheader("📌 Job Type Distribution")

if job_type_col is not None:

    type_data = (
        df[job_type_col]
        .astype(str)
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    type_data.columns = [
        "Job Type",
        "Jobs"
    ]

    st.bar_chart(
        type_data.set_index("Job Type")
    )

    st.dataframe(
        type_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HOURLY RATE ANALYSIS
# ============================================================

st.subheader("💰 Hourly Rate Analysis")

if rate_col is not None:

    rate_df = pd.DataFrame({
        "Hourly Rate": rate_series
    })

    rate_df = rate_df.dropna()

    if not rate_df.empty:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
            "Minimum Rate",
            f"${rate_df['Hourly Rate'].min():,.2f}"
        )

        with c2:
            st.metric(
            "Average Rate",
            f"${rate_df['Hourly Rate'].mean():,.2f}"
        )

        with c3:
            st.metric(
            "Maximum Rate",
            f"${rate_df['Hourly Rate'].max():,.2f}"
        )

        st.line_chart(
            rate_df.head(100)
        )

    else:

        st.warning(
            "Hourly rate column exists, but no numeric rate values were found."
        )

else:

    st.warning(
        "Hourly rate column was not detected."
    )


# ============================================================
# JOB RECOMMENDATION
# ============================================================

st.subheader("🎯 Job Recommendation")
st.write("Enter your skills below to find jobs that match your profile.")

user_skills = st.text_input(
    "Your Skills",
    placeholder="Example: Python, SQL, Power BI, Excel, Data Analysis"
)

# Detect job title and description columns
title_col = None
description_col = None

for col in df.columns:
    col_clean = str(col).strip().lower()

    if title_col is None and col_clean in [
        "title",
        "job title",
        "job_title",
        "jobtitle"
    ]:
        title_col = col

    if description_col is None and col_clean in [
        "description",
        "job description",
        "job_description",
        "jobdescription"
    ]:
        description_col = col

# Your dataset has title column = "title"

if title_col is None and "title" in df.columns:
    title_col = "title"

if title_col is not None:

    search_df = df.copy()

    search_df["_search_text"] = (
        search_df[title_col]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    if description_col is not None:
        search_df["_search_text"] = (
            search_df["_search_text"]
            + " "
            + search_df[description_col]
            .fillna("")
            .astype(str)
            .str.lower()
        )

if user_skills.strip():

    skills = [
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    ]

    # Get recommendations
    recommendations = get_recommendations(df, user_skills)

    st.subheader(
        f" 🔎 Matching Jobs: {len(recommendations)}"
    )

    if not recommendations.empty:

        # Columns we would like to display
        display_cols = []

        # Job title
        if title_col in recommendations.columns:
            display_cols.append(title_col)

        # Country
        if "country" in recommendations.columns:
            display_cols.append("country")

        # Job type
        if "job_type" in recommendations.columns:
            display_cols.append("job_type")

        # Budget
        if "budget" in recommendations.columns:
            display_cols.append("budget")

        # Average hourly rate
        if "average_hourly_rate" in recommendations.columns:
            display_cols.append("average_hourly_rate")

        # Match score
        if "match_score" in recommendations.columns:
            display_cols.append("match_score")

        # Job link
        if "link" in recommendations.columns:
            display_cols.append("link")

    # Keep only columns that actually exist
    display_cols = [
        col for col in display_cols
        if col in recommendations.columns
    ]

# Show results

recommendations = pd.DataFrame()

if user_skills.strip():
    skills = [
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    ]

    recommendations = get_recommendations(df, user_skills)

    if "match_score" in recommendations.columns:
        min_match_score = st.slider(
            "Minimum Match Score (%)",
            min_value=0,
            max_value=100,
            value=60,
            step=5
        )
        recommendations = recommendations[
            recommendations["match_score"] >= min_match_score
        ]

    if "country" in recommendations.columns:
        countries = ["All Countries"] + sorted(
            recommendations["country"]
            .dropna()
            .unique()
            .tolist()
        )
        selected_country = st.selectbox("Select Country", countries)
        
        if selected_country != "All Countries":
            recommendations = recommendations[
                recommendations["country"] == selected_country
            ]
    if "job_type" in recommendations.columns:
        job_types = ["All Job Types"] + sorted(
            recommendations["job_type"]
            .dropna()
            .unique()
            .tolist()
        )
        selected_job_type = st.selectbox("Select Job Type", job_types)
        
        if selected_job_type != "All Job Types":
            recommendations = recommendations[
                recommendations["job_type"] == selected_job_type
            ]


# Hourly Rate Filter

if "average_hourly_rate" in recommendations.columns:
    hourly_values = pd.to_numeric(
        recommendations["average_hourly_rate"],
        errors="coerce"
    ).dropna()

    if len(hourly_values) > 0:
        min_rate = float(hourly_values.min())
        max_rate = float(hourly_values.max())

        if min_rate < max_rate:
            rate_range = st.slider(
                "💵 Hourly Rate Range",
                min_value=min_rate,
                max_value=max_rate,
                value=(min_rate, max_rate),
                step=1.0
            )

            recommendations = recommendations[
                pd.to_numeric(
                    recommendations["average_hourly_rate"],
                    errors="coerce"
                ).between(
                    rate_range[0],
                    rate_range[1]
                )
                | recommendations["average_hourly_rate"].isna()
            ]

# Budget Range Filter

if "budget" in recommendations.columns:
    budget_values = pd.to_numeric(
        recommendations["budget"],
        errors="coerce"
    ).dropna()

    if len(budget_values) > 0:
        min_budget = float(budget_values.min())
        max_budget = float(budget_values.max())

        if min_budget < max_budget:
            budget_range = st.slider(
                "💰 Budget Range",
                min_value=min_budget,
                max_value=max_budget,
                value=(min_budget, max_budget),
                step=1.0
            )
        else: 
            st.info(f"💰 Fixed Price Budget: {min_budget:2f}")
            budget_range = (min_budget, max_budget)        

            recommendations = recommendations[
                pd.to_numeric(
                    recommendations["budget"],
                    errors="coerce"
                ).between(
                    budget_range[0],
                    budget_range[1]
                )
                | recommendations["budget"].isna()
            ]

# Sort Jobs

sort_option = st.selectbox(
    "Sort Jobs By",
    [
        "match Score (low to high)",
        "Match Score (High to Low)",
        "Hourly Rate (High to Low)",
        "Hourly Rate (Low to High)",
        "Budget (High to Low)",
        "Budget (Low to High)"
    ]
)

if not recommendations.empty and "match_score" in recommendations.columns:

    if sort_option == "Match Score (High to Low)":
        recommendations = recommendations.sort_values(
            "match_score",
            ascending=False
        )

    elif sort_option == "Match Score (Low to High)":
        recommendations = recommendations.sort_values(
            "match_score",
            ascending=True
        )

    elif (
        sort_option == "Hourly Rate (High to Low)"
        and "average_hourly_rate" in recommendations.columns
    ):
        recommendations = recommendations.sort_values(
            "average_hourly_rate",
            ascending=False
        )

    elif (
        sort_option == "Hourly Rate (Low to High)"
        and "average_hourly_rate" in recommendations.columns
    ):
        recommendations = recommendations.sort_values(
            "average_hourly_rate",
            ascending=True
        )

# Job Title Search Filter

job_search = st.text_input(
    "Search Job Title",
    placeholder="e.g. Data Analyst, Python, Power BI"
)

if job_search:
    recommendations = recommendations[
        recommendations[title_col]
        .astype(str)
        .str.contains(job_search, case=False, na=False)
    ]

    display_cols = [
    col for col in [
        title_col,
        "country",
        "job_type",
        "budget",
        "average_hourly_rate",
        "match_score",
        "link"
    ]
    if col in recommendations.columns    
]

    if display_cols:
        result_df = recommendations[display_cols].head(20).copy()

    rename_map = {
        title_col: "Job Title",
        "country": "Country",
        "job_type": "Job Type",
        "budget": "Budget",
        "average_hourly_rate": "Hourly Rate",
        "match_score": "Match Score (%)",
        "link": "Job Link"
    }

    result_df = result_df.rename(columns=rename_map)

    st.dataframe(
        result_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Job Link": st.column_config.LinkColumn(
                "Apply Now",
                display_text="Apply"
            ),
            "Match Score (%)": st.column_config.NumberColumn(
                "Match Score (%)",
                format="%.2f%%"
            ),
            "Budget": st.column_config.NumberColumn(
                "Budget",
                format="%.2f"
            ),
            "Hourly Rate": st.column_config.NumberColumn(
                "Hourly Rate",
                format="%.2f"
            )
        }
    )

else:
    st.warning("No displayable job information found.")

# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("🔍 View Dataset Information"):

    st.write(
        f"Rows: **{df.shape[0]:,}**"
    )

    st.write(
        f"Columns: **{df.shape[1]:,}**"
    )

    st.write("Detected columns:")

    st.write(
        df.columns.tolist()
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Job Market Analysis & Recommendation Dashboard")

# ============================================================
# TASK 6: MONTHLY JOB MARKET DYNAMICS
# ============================================================

st.markdown("---")
st.header("📅 Monthly Job Market Dynamics")

monthly_file = "analysis_output/monthly_job_demand.csv"

if os.path.exists(monthly_file):

    monthly_data = pd.read_csv(monthly_file)

    monthly_data["month"] = pd.to_datetime(
        monthly_data["month"],
        errors="coerce"
    )

    monthly_data = monthly_data.dropna(
        subset=["month"]
    ).sort_values("month")

    # Monthly job-posting trend
    st.subheader("📈 Job Posting Trend Over Time")

    st.line_chart(
        monthly_data.set_index("month")["job_count"]
    )

    # Latest month information
    latest_month = monthly_data.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latest Month",
            latest_month["month"].strftime("%B %Y")
        )

    with col2:
        st.metric(
            "Jobs Posted",
            f"{int(latest_month['job_count']):,}"
        )

    with col3:
        if len(monthly_data) > 1:

            previous_month = monthly_data.iloc[-2]

            change = (
                latest_month["job_count"]
                - previous_month["job_count"]
            )

            st.metric(
                "Change vs Previous Month",
                f"{int(change):,}",
                delta=f"{int(change):,}"
            )

    # Monthly data table
    st.subheader("📊 Monthly Job Market Data")

    display_monthly = monthly_data.copy()

    display_monthly["month"] = (
        display_monthly["month"]
        .dt.strftime("%B %Y")
    )

    st.dataframe(
        display_monthly,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning(
        "Monthly job demand data was not found. "
        "Run analysis.py first."
    )

    