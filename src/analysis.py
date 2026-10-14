import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/cleaned_jobs.csv")

print("\nAvailable columns:")
print(df.columns.tolist())

print("Dataset shape:", df.shape)

# Create output folder
import os
os.makedirs("analysis_output", exist_ok=True)

# ============================================================
# TASK 1: JOB-TITLE KEYWORDS vs COMPENSATION
# ============================================================

import re

keywords = [
    "python",
    "data analyst",
    "data scientist",
    "power bi",
    "sql",
    "machine learning",
    "developer",
    "designer",
    "marketing",
    "virtual assistant"
]

keyword_results = []

for keyword in keywords:
    mask = df["title"].fillna("").str.contains(
        re.escape(keyword),
        case=False,
        regex=True
    )

    matched_jobs = df[mask]

    hourly_jobs = matched_jobs[
        pd.to_numeric(
            matched_jobs["average_hourly_rate"],
            errors="coerce"
        ).notna()
    ]

    avg_rate = pd.to_numeric(
        hourly_jobs["average_hourly_rate"],
        errors="coerce"
    ).mean()

    keyword_results.append({
        "Keyword": keyword,
        "Job Count": len(matched_jobs),
        "Average Hourly Rate": round(avg_rate, 2)
    })

keyword_analysis = pd.DataFrame(keyword_results)

print("\nKeyword Compensation Analysis:")
print(keyword_analysis)

# Save results
keyword_analysis.to_csv(
    "analysis_output/keyword_compensation_analysis.csv",
    index=False
)
# Plot
plot_data = keyword_analysis.dropna(
    subset=["Average Hourly Rate"]
).sort_values(
    "Average Hourly Rate"
)

plt.figure(figsize=(10, 6))
plt.barh(
    plot_data["Keyword"],
    plot_data["Average Hourly Rate"]
)

plt.title("Average Hourly Rate by Job-Title Keyword")
plt.xlabel("Average Hourly Rate")
plt.ylabel("Job-Title Keyword")
plt.tight_layout()

plt.savefig(
    "analysis_output/keyword_hourly_rate.png"
)

plt.show()

# -----------------------------------
# 1. Top Job Titles
# -----------------------------------

top_titles = df["title"].value_counts().head(15)

print("\nTop Job Titles:")
print(top_titles)

plt.figure(figsize=(10, 6))
top_titles.sort_values().plot(kind="barh")
plt.title("Top 15 Job Titles")
plt.xlabel("Number of Jobs")
plt.ylabel("Job Title")
plt.tight_layout()
plt.savefig("analysis_output/top_job_titles.png")
plt.show()

# ============================================================
# 2. Country + Job Type Compensation Analysis
# ============================================================

# Convert hourly rate to numeric
df["average_hourly_rate"] = pd.to_numeric(
    df["average_hourly_rate"],
    errors="coerce"
)

# Remove rows without country, job type, or hourly rate
compensation_data = df.dropna(
    subset=["country", "job_type", "average_hourly_rate"]
).copy()

# Calculate average hourly rate by Country and Job Type
country_job_analysis = (
    compensation_data
    .groupby(["country", "job_type"])
    .agg(
        Job_Count=("title", "count"),
        Average_Hourly_Rate=("average_hourly_rate", "mean")
    )
    .reset_index()
)

country_job_analysis["Average_Hourly_Rate"] = (
    country_job_analysis["Average_Hourly_Rate"].round(2)
)

# Sort by highest average hourly rate
country_job_analysis = country_job_analysis.sort_values(
    "Average_Hourly_Rate",
    ascending=False
)

print("\nCountry + Job Type Compensation Analysis:")
print(country_job_analysis.head(20))

# Save results
country_job_analysis.to_csv(
    "analysis_output/country_job_type_compensation.csv",
    index=False
)

# Top 15 country/job-type combinations
top_combinations = country_job_analysis.head(15).copy()

top_combinations["Combination"] = (
    top_combinations["country"]
    + " - "
    + top_combinations["job_type"]
)

# Create chart
plt.figure(figsize=(11, 7))

plt.barh(
    top_combinations["Combination"],
    top_combinations["Average_Hourly_Rate"]
)

plt.title("Top Country + Job Type Combinations by Hourly Rate")
plt.xlabel("Average Hourly Rate")
plt.ylabel("Country - Job Type")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "analysis_output/country_job_type_compensation.png"
)

plt.show()


# -----------------------------------
# 2. Top Countries
# -----------------------------------

top_countries = df["country"].value_counts().head(15)

print("\nTop Countries:")
print(top_countries)

plt.figure(figsize=(10, 6))
top_countries.sort_values().plot(kind="barh")
plt.title("Top 15 Countries by Job Count")
plt.xlabel("Number of Jobs")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("analysis_output/top_countries.png")
plt.show()


# -----------------------------------
# 3. Hourly vs Fixed Price
# -----------------------------------

job_types = df["job_type"].value_counts()

print("\nJob Type:")
print(job_types)

plt.figure(figsize=(7, 5))
job_types.plot(kind="pie", autopct="%1.1f%%")
plt.title("Hourly vs Fixed Price Jobs")
plt.ylabel("")
plt.tight_layout()
plt.savefig("analysis_output/job_type_distribution.png")
plt.show()


# -----------------------------------
# 4. Average Hourly Rate
# -----------------------------------

hourly_data = df["average_hourly_rate"].dropna()

print("\nHourly Rate Statistics:")
print(hourly_data.describe())

plt.figure(figsize=(10, 6))
plt.hist(hourly_data, bins=30)
plt.title("Distribution of Average Hourly Rates")
plt.xlabel("Average Hourly Rate")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.savefig("analysis_output/hourly_rate_distribution.png")
plt.show()


# -----------------------------------
# 5. Budget Distribution
# -----------------------------------

budget_data = df["budget"].dropna()

print("\nBudget Statistics:")
print(budget_data.describe())

plt.figure(figsize=(10, 6))
plt.hist(budget_data, bins=30)
plt.title("Distribution of Job Budgets")
plt.xlabel("Budget")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.savefig("analysis_output/budget_distribution.png")
plt.show()


print("\n================================")
print("JOB MARKET ANALYSIS COMPLETED!")
print("Charts saved in: analysis_output/")
print("================================")

# ============================================================
# 3. Job Title Compensation Analysis
# ============================================================

print("\nJob Title Compensation Analysis:")

title_compensation = (
    df.dropna(subset=["title", "average_hourly_rate"])
      .groupby("title")
      .agg(
          job_count=("title", "count"),
          average_hourly_rate=("average_hourly_rate", "mean")
      )
      .query("job_count >= 10")
      .sort_values("average_hourly_rate", ascending=False)
      .head(15)
)

print(title_compensation)

# Save results
title_compensation.to_csv(
    "analysis_output/job_title_compensation.csv"
)

# Create chart
plt.figure(figsize=(10, 6))

title_compensation["average_hourly_rate"].sort_values().plot(
    kind="barh"
)

plt.title("Top Job Titles by Average Hourly Rate")
plt.xlabel("Average Hourly Rate")
plt.ylabel("Job Title")
plt.tight_layout()

plt.savefig(
    "analysis_output/job_title_compensation.png"
)

plt.show()

# ============================================================
# 4. Job Demand vs Compensation Analysis
# ============================================================

print("\nJob Demand vs Compensation Analysis:")

demand_compensation = (
    df.dropna(subset=["title", "average_hourly_rate"])
      .groupby("title")
      .agg(
          job_count=("title", "count"),
          average_hourly_rate=("average_hourly_rate", "mean")
      )
)

# Keep job titles with at least 10 jobs
demand_compensation = demand_compensation[
    demand_compensation["job_count"] >= 10
].copy()

# Sort by job demand
top_demand = demand_compensation.sort_values(
    "job_count",
    ascending=False
).head(15)

print(top_demand)

# Save analysis
top_demand.to_csv(
    "analysis_output/job_demand_compensation.csv"
)

# Create scatter plot
plt.figure(figsize=(10, 6))

plt.scatter(
    top_demand["job_count"],
    top_demand["average_hourly_rate"]
)

plt.xlabel("Number of Jobs")
plt.ylabel("Average Hourly Rate")
plt.title("Job Demand vs Average Hourly Rate")

plt.tight_layout()

plt.savefig(
    "analysis_output/job_demand_vs_compensation.png"
)

plt.show()

# ============================================================
# 5. Country-wise Job Demand & Compensation Analysis
# ============================================================

print("\nCountry-wise Job Demand & Compensation:")

country_analysis = (
    df.dropna(subset=["country", "average_hourly_rate"])
      .groupby("country")
      .agg(
          job_count=("country", "count"),
          average_hourly_rate=("average_hourly_rate", "mean")
      )
      .query("job_count >= 20")
      .sort_values("job_count", ascending=False)
)

print(country_analysis.head(15))

# Save results
country_analysis.to_csv(
    "analysis_output/country_demand_compensation.csv"
)

# Top 15 countries by job demand
top_countries = country_analysis.head(15)

plt.figure(figsize=(10, 6))

top_countries["job_count"].sort_values().plot(
    kind="barh"
)

plt.title("Top Countries by Job Demand")
plt.xlabel("Number of Jobs")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    "analysis_output/country_job_demand.png"
)

plt.show()

# ============================================================
# 6. Skill / Keyword Demand Analysis
# ============================================================

print("\nSkill / Keyword Demand Analysis:")

keywords = [
    "python",
    "sql",
    "power bi",
    "data analyst",
    "data scientist",
    "machine learning",
    "developer",
    "designer",
    "marketing",
    "virtual assistant"
]

keyword_demand = []

for keyword in keywords:

    mask = df["title"].fillna("").str.lower().str.contains(
        keyword,
        regex=False
    )

    keyword_demand.append({
        "keyword": keyword,
        "job_count": mask.sum()
    })

keyword_demand_df = pd.DataFrame(keyword_demand)

keyword_demand_df = keyword_demand_df.sort_values(
    "job_count",
    ascending=False
)

print(keyword_demand_df)

# Save results
keyword_demand_df.to_csv(
    "analysis_output/skill_keyword_demand.csv",
    index=False
)

# Create chart
plt.figure(figsize=(10, 6))

keyword_demand_df.sort_values(
    "job_count"
).plot(
    x="keyword",
    y="job_count",
    kind="barh",
    legend=False,
    figsize=(10, 6)
)

plt.title("Most In-Demand Skills / Job Keywords")
plt.xlabel("Number of Jobs")
plt.ylabel("Skill / Keyword")

plt.tight_layout()

plt.savefig(
    "analysis_output/skill_keyword_demand.png"
)

plt.show()

# ============================================================
# TASK 3: HIGH-DEMAND JOB ROLE PREDICTION
# ============================================================

# Convert published date
df["published_date"] = pd.to_datetime(
    df["published_date"],
    errors="coerce"
)

# Remove invalid dates
date_df = df.dropna(
    subset=["published_date", "title"]
).copy()

# Create monthly period
date_df["month"] = (
    date_df["published_date"]
    .dt.to_period("M")
    .astype(str)
)

# Monthly job demand
monthly_demand = (
    date_df
    .groupby("month")
    .size()
    .reset_index(name="job_count")
)

print("\nMonthly Job Demand:")
print(monthly_demand.tail(12))

# Save monthly demand data
monthly_demand.to_csv(
    "analysis_output/monthly_job_demand.csv",
    index=False
)

# Plot demand over time
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_demand["month"],
    monthly_demand["job_count"]
)

plt.title("Job Posting Demand Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Job Postings")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "analysis_output/monthly_job_demand.png"
)

plt.show()

# ============================================================
# TASK 3: PREDICT FUTURE JOB DEMAND
# ============================================================

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Create numeric time index
model_data = monthly_demand.copy()

model_data["time_index"] = range(len(model_data))

# Features and target
X = model_data[["time_index"]]
y = model_data["job_count"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nPrediction Model Performance:")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 4))

# Save predictions
test_results = X_test.copy()
test_results["Actual Job Count"] = y_test.values
test_results["Predicted Job Count"] = y_pred.round(0)

test_results.to_csv(
    "analysis_output/job_demand_predictions.csv",
    index=False
)

# ============================================================
# FUTURE JOB DEMAND FORECAST
# ============================================================

future_periods = 6

last_index = model_data["time_index"].max()

future_index = np.arange(
    last_index + 1,
    last_index + 1 + future_periods
).reshape(-1, 1)

future_predictions = model.predict(future_index)

last_month = pd.Period(
    monthly_demand["month"].iloc[-1],
    freq="M"
)

future_months = pd.period_range(
    start=last_month + 1,
    periods=future_periods,
    freq="M"
)

future_forecast = pd.DataFrame({
    "Future_Period": future_months.astype(str),
    "Predicted_Job_Demand": future_predictions.round(0)
})

print("\nFuture Job Demand Forecast:")
print(future_forecast)

future_forecast.to_csv(
    "analysis_output/future_job_demand_forecast.csv",
    index=False
)

# ============================================================
# ACTUAL vs PREDICTED DEMAND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    y_test.values,
    label="Actual Demand"
)

plt.plot(
    y_pred,
    label="Predicted Demand"
)

plt.title("Actual vs Predicted Job Demand")
plt.xlabel("Test Sample")
plt.ylabel("Number of Job Postings")

plt.legend()
plt.tight_layout()

plt.savefig(
    "analysis_output/actual_vs_predicted_demand.png"
)

plt.show()

# ============================================================
# TASK 3: HIGH-DEMAND JOB ROLES
# ============================================================

print("\nHigh-Demand Job Roles:")

role_demand = (
    date_df
    .groupby("title")
    .size()
    .reset_index(name="job_count")
)

# Remove very rare job titles
role_demand = role_demand[
    role_demand["job_count"] >= 10
].copy()

# Select top 20 roles
top_roles = (
    role_demand
    .sort_values(
        "job_count",
        ascending=False
    )
    .head(20)
)

print(top_roles)

# Save result
top_roles.to_csv(
    "analysis_output/high_demand_job_roles.csv",
    index=False
)

# ============================================================
# HIGH-DEMAND JOB ROLES VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 8))

plt.barh(
    top_roles["title"].iloc[::-1],
    top_roles["job_count"].iloc[::-1]
)

plt.title("Top 20 High-Demand Job Roles")
plt.xlabel("Number of Job Postings")
plt.ylabel("Job Title")

plt.tight_layout()

plt.savefig(
    "analysis_output/high_demand_job_roles.png"
)

plt.show()

# ============================================================
# TASK 4: AVERAGE HOURLY RATE ACROSS COUNTRIES
# ============================================================

import plotly.express as px

print("\nCountry-wise Average Hourly Rate:")

# Convert hourly rate to numeric
df["average_hourly_rate"] = pd.to_numeric(
    df["average_hourly_rate"],
    errors="coerce"
)

# Country analysis
country_hourly = (
    df.dropna(
        subset=["country", "average_hourly_rate"]
    )
    .groupby("country")
    .agg(
        job_count=("title", "count"),
        average_hourly_rate=("average_hourly_rate", "mean")
    )
    .reset_index()
)

# Round values
country_hourly["average_hourly_rate"] = (
    country_hourly["average_hourly_rate"].round(2)
)

# Remove countries with very few jobs
country_hourly = country_hourly[
    country_hourly["job_count"] >= 10
].copy()

# Sort by hourly rate
country_hourly = country_hourly.sort_values(
    "average_hourly_rate",
    ascending=False
)

print(country_hourly.head(20))

print("========== TASK 4 REACHED ==========")

# Save country analysis
country_hourly.to_csv(
    "analysis_output/country_average_hourly_rate.csv",
    index=False
)

# ============================================================
# INTERACTIVE COUNTRY MAP
# ============================================================

fig = px.choropleth(
    country_hourly,
    locations="country",
    locationmode="country names",
    color="average_hourly_rate",
    hover_name="country",
    hover_data={
        "job_count": True,
        "average_hourly_rate": ":.2f"
    },
    title="Average Hourly Rate by Country",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True
    )
)

fig.write_html(
    "analysis_output/country_hourly_rate_map.html"
)

fig.show()

# ============================================================
# TASK 2: EMERGING JOB CATEGORIES
# ============================================================

print("\nEmerging Job Categories:")

# Create job categories from job titles
def categorize_job(title):

    title = str(title).lower()

    if any(x in title for x in [
        "data analyst", "data scientist", "data engineer",
        "machine learning", "artificial intelligence",
        "ai ", "business analyst"
    ]):
        return "Data & AI"

    elif any(x in title for x in [
        "developer", "software engineer", "web developer",
        "frontend", "backend", "full stack"
    ]):
        return "Software Development"

    elif any(x in title for x in [
        "designer", "graphic design", "ui/ux", "ux", "ui designer"
    ]):
        return "Design"

    elif any(x in title for x in [
        "marketing", "seo", "social media", "digital marketing"
    ]):
        return "Marketing"

    elif any(x in title for x in [
        "virtual assistant", "administrative assistant",
        "executive assistant", "data entry"
    ]):
        return "Administrative & Support"

    elif any(x in title for x in [
        "sales", "business development"
    ]):
        return "Sales & Business Development"

    elif any(x in title for x in [
        "writer", "content", "copywriter", "blog"
    ]):
        return "Writing & Content"

    else:
        return "Other"

# Apply categories
date_df["job_category"] = date_df["title"].apply(
    categorize_job
)

# Monthly category demand
category_monthly = (
    date_df
    .groupby(["month", "job_category"])
    .size()
    .reset_index(name="job_count")
)

# Save monthly category data
category_monthly.to_csv(
    "analysis_output/emerging_categories_monthly.csv",
    index=False
)

# ============================================================
# CATEGORY GROWTH ANALYSIS
# ============================================================

category_growth = (
    category_monthly
    .groupby("job_category")["job_count"]
    .agg(
        total_jobs="sum",
        first_month="first",
        latest_month="last"
    )
    .reset_index()
)

category_growth["growth"] = (
    category_growth["latest_month"]
    - category_growth["first_month"]
)

category_growth["growth_percent"] = (
    category_growth["growth"]
    / category_growth["first_month"].replace(0, 1)
    * 100
)

category_growth = category_growth.sort_values(
    "growth_percent",
    ascending=False
)

print("\nCategory Growth Analysis:")
print(category_growth)

# Save results
category_growth.to_csv(
    "analysis_output/emerging_job_categories.csv",
    index=False
)

# ============================================================
# EMERGING CATEGORY VISUALIZATION
# ============================================================

top_emerging = category_growth.head(10)

plt.figure(figsize=(11, 7))

plt.barh(
    top_emerging["job_category"].iloc[::-1],
    top_emerging["growth_percent"].iloc[::-1]
)

plt.title("Emerging Job Categories by Growth")
plt.xlabel("Growth (%)")
plt.ylabel("Job Category")

plt.tight_layout()

plt.savefig(
    "analysis_output/emerging_job_categories.png"
)

plt.show()

# ============================================================
# TASK 3: HIGH-DEMAND JOB ROLE PREDICTION
# ============================================================

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

print("\n" + "=" * 60)
print("TASK 3: HIGH-DEMAND JOB ROLE PREDICTION")
print("=" * 60)

# Use monthly job demand
prediction_data = monthly_demand.copy()

# Create numerical month index
prediction_data["month_number"] = np.arange(
    len(prediction_data)
)

# Remove invalid values
prediction_data = prediction_data.dropna(
    subset=["job_count"]
).copy()

# Features and target
X = prediction_data[
    ["month_number"]
]

y = prediction_data[
    "job_count"
]

# Check whether enough data exists
if len(prediction_data) >= 5:

    # Chronological train/test split
    split_index = int(
        len(prediction_data) * 0.8
    )

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # Create model
    model = LinearRegression()

    # Train
    model.fit(
        X_train,
        y_train
    )

    # Predict
    y_pred = model.predict(
        X_test
    )

    # Accuracy metrics
    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred
        )
    )

    print("\nPrediction Accuracy:")

    print(
        "MAE:",
        round(mae, 2)
    )

    print(
        "RMSE:",
        round(rmse, 2)
    )

    # Prediction results
    prediction_results = pd.DataFrame({
        "Month": prediction_data.iloc[
            split_index:
        ]["month"].values,
        "Actual Jobs": y_test.values,
        "Predicted Jobs": np.round(
            y_pred,
            0
        )
    })

    print("\nJob Demand Predictions:")

    print(
        prediction_results
    )

    # Save predictions
    prediction_results.to_csv(
        "analysis_output/job_demand_predictions.csv",
        index=False
    )

    # Plot actual vs predicted
    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        prediction_results["Month"],
        prediction_results["Actual Jobs"],
        marker="o",
        label="Actual Jobs"
    )

    plt.plot(
        prediction_results["Month"],
        prediction_results["Predicted Jobs"],
        marker="o",
        linestyle="--",
        label="Predicted Jobs"
    )

    plt.title(
        "Actual vs Predicted Job Demand"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Number of Job Postings"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "analysis_output/actual_vs_predicted_demand.png"
    )
    plt.show()

else:

    print(
        "\nNot enough monthly data "
        "to train the prediction model."
    )

# ============================================================
# TASK 7: REMOTE-WORK LANDSCAPE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TASK 7: REMOTE-WORK LANDSCAPE ANALYSIS")
print("=" * 60)

# Remote-work proxy based on job-title keywords
remote_keywords = [
    "remote",
    "work from home",
    "wfh",
    "work-from-home",
    "virtual"
]

title_text = df["title"].fillna("").astype(str).str.lower()

remote_mask = title_text.str.contains(
    "|".join(remote_keywords),
    regex=True
)

df["work_mode_proxy"] = np.where(
    remote_mask,
    "Remote",
    "Not Explicitly Remote"
)

# Overall remote-work summary
remote_summary = (
    df["work_mode_proxy"]
    .value_counts()
    .reset_index()
)

remote_summary.columns = [
    "Work Mode",
    "Job Count"
]

remote_summary["Percentage"] = (
    remote_summary["Job Count"]
    / remote_summary["Job Count"].sum()
    * 100
).round(2)

print("\nRemote Work Summary:")
print(remote_summary)

remote_summary.to_csv(
    "analysis_output/remote_work_summary.csv",
    index=False
)

# Monthly remote-work trend
remote_df = df.dropna(
    subset=["published_date"]
).copy()

remote_df["month"] = (
    pd.to_datetime(
        remote_df["published_date"],
        errors="coerce"
    )
    .dt.to_period("M")
    .astype(str)
)

remote_monthly = (
    remote_df
    .groupby(["month", "work_mode_proxy"])
    .size()
    .reset_index(name="job_count")
)

remote_monthly.to_csv(
    "analysis_output/remote_work_monthly.csv",
    index=False
)

# Remote jobs only
remote_only = remote_monthly[
    remote_monthly["work_mode_proxy"] == "Remote"
].copy()

# Plot
plt.figure(figsize=(12, 6))

if not remote_only.empty:
    plt.plot(
        remote_only["month"],
        remote_only["job_count"],
        marker="o"
    )

plt.title("Remote Job Posting Trend Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Remote Job Postings")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "analysis_output/remote_job_trend.png"
)

plt.show()

# ============================================================
# TASK 8: FUTURE JOB-MARKET TREND ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TASK 8: FUTURE JOB-MARKET TREND ANALYSIS")
print("=" * 60)

# Load the future demand forecast created earlier
forecast_path = "analysis_output/future_job_demand_forecast.csv"

if os.path.exists(forecast_path):

    future_forecast = pd.read_csv(forecast_path)

    # Display forecast
    print("\nFuture Job Demand Forecast:")
    print(future_forecast)

    # Calculate forecast growth
    first_value = future_forecast[
        "Predicted_Job_Demand"
    ].iloc[0]

    last_value = future_forecast[
        "Predicted_Job_Demand"

    ].iloc[-1]

    if first_value != 0:
        growth_percentage = (
            (last_value - first_value) / abs(first_value)
        ) * 100
    else:
        growth_percentage = 0

    print(
        f"\nForecast change across the period: "
        f"{growth_percentage:.2f}%"
    )

    # Save trend summary
    trend_summary = pd.DataFrame({
        "Metric": [
            "First Forecast Demand",
            "Last Forecast Demand",
            "Forecast Change Percentage"
        ],
        "Value": [
            first_value,
            last_value,
            round(growth_percentage, 2)
        ]
    })

    trend_summary.to_csv(
        "analysis_output/future_trend_summary.csv",
        index=False
    )

    # Plot future trend
    plt.figure(figsize=(10, 6))

    plt.plot(
        future_forecast["Future_Period"],
        future_forecast["Predicted_Job_Demand"],
        marker="o"
    )

    plt.title("Future Job-Market Demand Forecast")
    plt.xlabel("Future Month")
    plt.ylabel("Predicted Job Postings")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "analysis_output/future_job_market_trend.png"
    )

    plt.show()

    print("\nTask 8 outputs saved successfully.")

else:
    print(
        "\nForecast file not found. "
        "Run the earlier forecasting section first."
    )