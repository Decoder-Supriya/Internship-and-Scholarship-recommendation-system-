"""
recommender.py — ML Recommendation Engine
Uses TF-IDF + Cosine Similarity to match student profile to opportunities.

How it works (simple explanation):
1. We turn every opportunity into a "word fingerprint" using TF-IDF
2. We turn the student's profile into a word fingerprint too
3. We measure how similar each opportunity fingerprint is to the student's
4. We return the top N most similar opportunities
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data():
    """Load the CSV dataset into a pandas DataFrame."""
    df = pd.read_csv("dataset/opportunities.csv")
    return df


def build_opportunity_text(row):
    """
    Combine all relevant columns of an opportunity into one text string.
    This 'combined text' is what TF-IDF will analyze.
    """
    return " ".join([
        str(row["title"]),
        str(row["type"]),
        str(row["field"]),
        str(row["description"]),
        str(row["skills_required"]),
        str(row["location"]),
    ])


def build_student_text(profile):
    """
    Convert student profile dictionary into a single text string.
    This mirrors the structure of opportunity text for fair comparison.
    """
    text_parts = [
        profile.get("field_of_study", ""),
        profile.get("skills", ""),
        profile.get("interests", ""),
        profile.get("preferred_type", ""),   # 'scholarship' or 'internship' or 'both'
        profile.get("preferred_location", ""),
    ]
    return " ".join(text_parts)


def get_recommendations(profile, top_n=5):
    """
    Main function: takes a student profile dict, returns top_n recommendations.

    Args:
        profile (dict): Student profile with keys like field_of_study, skills, etc.
        top_n (int): Number of recommendations to return

    Returns:
        list: List of dicts, each representing a recommended opportunity
    """

    # --- Step 1: Load the dataset ---
    df = load_data()

    # --- Step 2: Apply CGPA filter ---
    # Both student CGPA and dataset min_gpa are on 10.0 scale — compare directly
    student_gpa = float(profile.get("gpa", 0.0))
    df = df[df["min_gpa"] <= student_gpa].copy()

    # --- Step 3: Apply type filter (scholarship / internship / both) ---
    preferred_type = profile.get("preferred_type", "both").lower()
    if preferred_type == "scholarship":
        df = df[df["type"] == "scholarship"]
    elif preferred_type == "internship":
        df = df[df["type"] == "internship"]
    # 'both' → no filter needed

    # --- Step 4: Handle edge case if no opportunities match ---
    if df.empty:
        return []

    # --- Step 5: Build text representations ---
    # Combine all opportunity columns into one text per row
    df["combined_text"] = df.apply(build_opportunity_text, axis=1)

    # Build the student's text profile
    student_text = build_student_text(profile)

    # --- Step 6: TF-IDF Vectorization ---
    # TF-IDF converts text into numerical vectors that represent word importance
    # It gives higher weight to words that are unique/specific (like "Python")
    # and lower weight to common words (like "the", "and")
    vectorizer = TfidfVectorizer(
        stop_words="english",    # Ignore common English words
        ngram_range=(1, 2),      # Consider 1-word and 2-word phrases
        max_features=500         # Keep top 500 most important terms
    )

    # Combine student text + all opportunity texts for vectorization
    all_texts = [student_text] + df["combined_text"].tolist()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Student vector = first row, opportunity vectors = rest
    student_vector = tfidf_matrix[0]
    opportunity_vectors = tfidf_matrix[1:]

    # --- Step 7: Cosine Similarity ---
    # Measures how similar the student's vector is to each opportunity's vector
    # Score ranges from 0 (no match) to 1 (perfect match)
    similarity_scores = cosine_similarity(student_vector, opportunity_vectors)[0]

    # --- Step 8: CGPA Bonus ---
    # Give a small bonus based on normalized GPA vs the opportunity's min_gpa
    gpa_bonus = np.minimum((student_gpa - df["min_gpa"].values) * 0.02, 0.15)
    final_scores = similarity_scores + gpa_bonus

    # --- Step 9: Rank and return top N results ---
    df = df.copy()
    df["match_score"] = final_scores
    df["match_percent"] = (final_scores * 100).round(1)

    # Sort by score descending and take top_n
    top_results = df.nlargest(top_n, "match_score")

    # Convert to list of dicts for easy JSON serialization
    results = []
    for _, row in top_results.iterrows():
        results.append({
            "id": int(row["id"]),
            "title": row["title"],
            "type": row["type"],
            "field": row["field"],
            "description": row["description"],
            "skills_required": row["skills_required"],
            "min_gpa": float(row["min_gpa"]),
            "location": row["location"],
            "amount": int(row["amount"]),
            "deadline": row["deadline"],
            "match_score": round(float(row["match_score"]), 3),
            "match_percent": float(row["match_percent"]),
        })

    return results


# ─── Quick test (run this file directly to test the model) ───────────────────
if __name__ == "__main__":
    test_profile = {
        "field_of_study": "Computer Science",
        "skills": "Python Machine Learning TensorFlow",
        "interests": "artificial intelligence deep learning data science",
        "gpa": 9.25,   # CGPA out of 10 (= ~3.7 on 4.0 scale)
        "preferred_type": "both",
        "preferred_location": "California USA",
    }

    recommendations = get_recommendations(test_profile, top_n=5)

    print("\n=== TOP RECOMMENDATIONS ===\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['type'].upper()}] {rec['title']}")
        print(f"   Field: {rec['field']} | Location: {rec['location']}")
        print(f"   Amount: ${rec['amount']} | Min GPA: {rec['min_gpa']}")
        print(f"   Match Score: {rec['match_percent']}%")
        print()