import pandas as pd

# Load dataset
df = pd.read_csv("data/job.csv")

print("Original shape:", df.shape)
print("Columns:", df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Clean text columns
df["country"] = df["country"].fillna("Unknown")
df["country"] = df["country"].astype(str).str.strip()

df["link"] = df["link"].astype(str).str.strip()

df["title"] = df["title"].astype(str).str.strip()

# Convert date
df["published_date"] = pd.to_datetime(
df["published_date"],
errors="coerce"
)

# Convert numeric columns
df["hourly_low"] = pd.to_numeric(
df["hourly_low"],
errors="coerce"
)

df["hourly_high"] = pd.to_numeric(
df["hourly_high"],
errors="coerce"
)

df["budget"] = pd.to_numeric(
df["budget"],
errors="coerce"
)

# Average hourly rate
df["average_hourly_rate"] = (
df["hourly_low"] + df["hourly_high"]
) / 2

# Job type
df["job_type"] = df["is_hourly"].map({
True: "Hourly",
False: "Fixed Price"
})

# Save cleaned dataset
df.to_csv(
"data/cleaned_jobs.csv",
index=False
)

print("Cleaned shape:", df.shape)
print("SUCCESS!")
print("Created: data/cleaned_jobs.csv")