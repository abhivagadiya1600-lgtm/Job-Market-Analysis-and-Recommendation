import pandas as pd

df = pd.read_csv("data/job.csv")

print("Original shape:", df.shape)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = df.drop_duplicates()

if "link" in df.columns:
    df = df.drop_duplicates(subset="link")

if "country" in df.columns:
    df["country"] = df["country"].fillna("Unknown")

if "published_date" in df.columns:
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")

for col in ["hourly_low", "hourly_high", "budget"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "hourly_low" in df.columns and "hourly_high" in df.columns:
    df["average_hourly_rate"] = df[["hourly_low", "hourly_high"]].mean(axis=1)

if "is_hourly" in df.columns:
    df["job_type"] = df["is_hourly"].map({True: "Hourly", False: "Fixed Price"})

df.to_csv("data/cleaned_jobs.csv", index=False)

print("Cleaned shape:", df.shape)
print("SUCCESS!")
print("Created: data/cleaned_jobs.csv")
