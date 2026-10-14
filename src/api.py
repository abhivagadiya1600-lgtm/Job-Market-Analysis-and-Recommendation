from fastapi import FastAPI, Query
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="Job Market Recommendation API",
    description="API for recommending jobs based on user skills.",
    version="1.0.0"
)

# Load cleaned dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "cleaned_jobs.csv"

df = pd.read_csv(DATA_PATH)

@app.get("/")
def home():
    return {
        "message": "Job Market Recommendation API is running",
        "version": "1.0.0"
    }

@app.get("/recommend")
def recommend_jobs(
    skills: str = Query(
        ...,
        description="Comma-separated skills, e.g. Python, SQL, Power BI"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=50
    )
):

    user_skills = [
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    ]

    recommendations = []

    for _, row in df.iterrows():

        title = str(row.get("title", "")).lower()

        matched_skills = [
            skill
            for skill in user_skills
            if skill in title
        ]

        if matched_skills:

            match_score = (
                len(matched_skills)
                / len(user_skills)
            ) * 100

            recommendations.append({
                "title": row.get("title",""),
                "country": row.get("country",""),
                "job_type": row.get("job_type",""),
                "average_hourly_rate": (
                    None
                    if pd.isna(row.get("average_hourly_rate"))
                    else float(row.get("average_hourly_rate"))
                ),
                "match_score": round(float(match_score), 2),
                "link": row.get("link")
            })

    result = pd.DataFrame(recommendations)

    if result.empty:
        return {
            "skills": user_skills,
            "recommendations": []
        }

    result = (
        result
        .sort_values(
            "match_score",
            ascending=False
        )
        .head(limit)
    )

    return {
        "skills": user_skills,
        "recommendations": result.fillna("").to_dict(
            orient="records"
        )
    }