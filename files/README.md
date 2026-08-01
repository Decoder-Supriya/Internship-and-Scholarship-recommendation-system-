# 🎓 Scholarship & Internship Recommendation System

A Machine Learning web app that recommends scholarships and internships based on a student's profile.

---

## 📁 Project Structure

```
scholarship_recommender/
│
├── dataset/
│   └── opportunities.csv       ← 50 scholarships & internships
│
├── templates/
│   └── index.html              ← The website (frontend)
│
├── recommender.py              ← ML model (TF-IDF + Cosine Similarity)
├── app.py                      ← Flask backend (web server)
├── requirements.txt            ← Python packages needed
└── README.md                   ← This file
```

---

## ⚙️ Setup Instructions (Step by Step)

### Step 1 — Install Python
Make sure Python 3.8+ is installed. Check by running:
```bash
python --version
```

### Step 2 — Create a Virtual Environment (recommended)
A virtual environment keeps your project packages separate.
```bash
# Create it
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 3 — Install Required Packages
```bash
pip install -r requirements.txt
```
This installs: Flask, pandas, scikit-learn, numpy.

### Step 4 — Run the Application
```bash
python app.py
```

You should see:
```
✅  Starting Scholarship/Internship Recommendation System
👉  Open your browser and go to:  http://localhost:5000
```

### Step 5 — Open the Website
Open your browser and go to:  **http://localhost:5000**

Fill in your profile and click "Find My Best Matches"! 🎉

---

## 🧠 How the ML Works (Simple Explanation)

1. **TF-IDF (Term Frequency-Inverse Document Frequency)**
   - Converts text (skills, interests, field) into numbers
   - Gives higher scores to specific/unique words like "TensorFlow" vs common words like "the"

2. **Cosine Similarity**
   - Measures how similar the student's text vector is to each opportunity's vector
   - Score from 0 (no match) to 1 (perfect match)

3. **GPA Filter**
   - Before ML runs, we remove opportunities where min GPA > student's GPA
   - Students only see opportunities they're eligible for

4. **GPA Bonus**
   - A small bonus is added if the student's GPA exceeds the minimum
   - This rewards strong students for over-qualifying

---

## 🧪 Test the ML Model Alone

You can test just the recommendation engine without the website:
```bash
python recommender.py
```

This runs a test profile and prints the top 5 recommendations.

---

## 🔧 Customizing the Dataset

To add more opportunities, open `dataset/opportunities.csv` and add rows.
Each row needs these columns:
- `id` — unique number
- `title` — name of scholarship/internship
- `type` — "scholarship" or "internship"
- `field` — subject area
- `description` — what it's about
- `skills_required` — space-separated skills
- `min_gpa` — minimum GPA required (e.g., 3.5)
- `location` — city/state/country
- `amount` — dollar amount
- `deadline` — YYYY-MM-DD format

---

## 🚀 Future Improvements You Can Add

- [ ] Add a database (SQLite) instead of CSV
- [ ] Add user login/signup system
- [ ] Add email alerts for deadline reminders
- [ ] Use collaborative filtering (recommend based on what similar students applied to)
- [ ] Deploy to the cloud (Heroku, Render, or AWS)
- [ ] Add more opportunities to the dataset

---

## 📦 Tech Stack

| Layer    | Technology           | Why              |
|----------|----------------------|------------------|
| ML Model | scikit-learn, pandas | TF-IDF + Cosine  |
| Backend  | Flask (Python)       | Simple REST API  |
| Frontend | HTML, CSS, JS        | No framework needed |
| Dataset  | CSV file             | Easy to edit     |
