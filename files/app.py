"""
app.py — Flask Backend API
Serves the HTML page and handles recommendation requests from the frontend.

Routes:
  GET  /           → serves the main webpage (index.html)
  POST /recommend  → accepts student profile JSON, returns recommendations
"""

import os
from flask import Flask, request, jsonify, render_template
from recommender import get_recommendations

# This makes Flask always find the templates folder
# relative to where app.py lives — not where you run the command from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))


@app.route("/")
def home():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Accepts a JSON body with student profile details.
    Returns a list of recommended scholarships/internships.

    Expected JSON body:
    {
        "field_of_study": "Computer Science",
        "skills": "Python Machine Learning",
        "interests": "AI deep learning",
        "gpa": 3.7,
        "preferred_type": "both",          // "scholarship", "internship", or "both"
        "preferred_location": "California"
    }
    """
    # Get JSON data from the request
    data = request.get_json()

    # Basic validation — make sure required fields are present
    required_fields = ["field_of_study", "skills", "gpa"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    # Validate GPA range
    try:
        gpa = float(data["gpa"])
        if not (0.0 <= gpa <= 10.0):
            return jsonify({"error": "CGPA must be between 0.0 and 10.0"}), 400
    except ValueError:
        return jsonify({"error": "CGPA must be a number"}), 400

    # Run the ML recommender
    try:
        recommendations = get_recommendations(data, top_n=5)
    except Exception as e:
        return jsonify({"error": f"Recommendation engine error: {str(e)}"}), 500

    # Return results as JSON
    return jsonify({
        "success": True,
        "count": len(recommendations),
        "recommendations": recommendations
    })


if __name__ == "__main__":
    # Run in debug mode during development (auto-restarts on code changes)
    print("\n✅  Starting Scholarship/Internship Recommendation System")
    print("👉  Open your browser and go to:  http://localhost:5000\n")
    app.run(debug=True, port=5000)