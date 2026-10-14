import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(df, user_skills, top_n=20):

    # Make a copy so the original dataframe is not changed
    data = df.copy()

    # Remove rows without a job title
    if "title" in data.columns:
        data = data.dropna(subset=["title"])

    # Columns used for job matching
    text_columns = [
        "title",
        "country",
        "job_type"
    ]

    # Add optional columns if they exist
    if "description" in data.columns:
        text_columns.append("description")

    if "skills" in data.columns:
        text_columns.append("skills")

    # Create search text
    data["search_text"] = ""

    for col in text_columns:
        if col in data.columns:
            data["search_text"] = (
                data["search_text"]
                + " "
                + data[col].fillna("").astype(str)
            )

    # Convert everything to lowercase
    data["search_text"] = data["search_text"].str.lower()

    # Clean user skills
    if isinstance(user_skills, str):
        query = user_skills.strip().lower()
    else:
        query = " ".join(
            str(skill).strip().lower()
            for skill in user_skills
        )

    # If no skills entered, return empty dataframe
    if not query:
        return pd.DataFrame()

    # TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    job_vectors = vectorizer.fit_transform(
        data["search_text"]
    )

    query_vector = vectorizer.transform(
        [query]
    )

    # Calculate similarity
    scores = cosine_similarity(
        query_vector,
        job_vectors
    ).flatten()

    # Add similarity score
    data["match_score"] = (
        scores * 100
    ).round(2)

    # Keep only jobs with actual similarity
    matching_indices = scores > 0

    matching_df = data.loc[
        matching_indices
    ].copy()

    matching_scores = scores[
        matching_indices
    ]

    # Sort by highest match
    sorted_positions = matching_scores.argsort()[::-1]

    # Top jobs
    results = matching_df.iloc[
        sorted_positions[:top_n]
    ].copy()

    # Add final score
    results["match_score"] = (
        matching_scores[sorted_positions[:top_n]] * 100
    ).round(2)

    return results
