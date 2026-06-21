from flask import Flask, render_template, request, flash
import json
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

# Load profile data
with open(os.path.join(os.path.dirname(__file__), "profile.json"), "r") as f:
    profile = json.load(f)

# Parse requirements.txt for skills page
def parse_requirements():
    skills = []
    req_path = os.path.join(os.path.dirname(__file__), "static", "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("#", 1)
                    dep = parts[0].strip()
                    desc = parts[1].strip() if len(parts) > 1 else ""
                    match = re.match(r"([A-Za-z0-9_-]+)([<>=]=?)([\d.]+)", dep)
                    if match:
                        skills.append({
                            "name": match.group(1),
                            "operator": match.group(2),
                            "level": match.group(3),
                            "description": desc
                        })
    return skills

@app.route("/")
def home():
    featured_projects = profile.get("projects", [])[:3]
    latest_posts = profile.get("blog_posts", [])[:2]
    skills = parse_requirements()
    total_projects = len(profile.get("projects", []))
    total_skills = len(skills)
    cloud_count = len(profile.get("skills", {}).get("Cloud & Virtualization", []))
    # Get max years
    max_years = 0
    for s in skills:
        try:
            max_years = max(max_years, int(float(s["level"])))
        except: pass
    return render_template("home.html", profile=profile,
                           featured_projects=featured_projects, latest_posts=latest_posts,
                           skills=skills, total_projects=total_projects, total_skills=total_skills,
                           cloud_count=cloud_count, max_years=max_years)

@app.route("/about")
def about():
    return render_template("about.html", profile=profile)

@app.route("/skills")
def skills_page():
    skills = parse_requirements()
    return render_template("skills.html", profile=profile, skills=skills)

@app.route("/experience")
def experience():
    return render_template("experience.html", profile=profile)

@app.route("/portfolio")
def portfolio():
    works = []
    for p in profile.get("projects", []):
        works.append({"type": "project", "name": p["name"], "description": p["description"], "tags": p.get("tags", []), "github": p.get("github")})
    return render_template("portfolio.html", profile=profile, works=works)

@app.route("/projects")
def projects_page():
    return render_template("projects.html", profile=profile)

@app.route("/blog")
def blog():
    return render_template("blog.html", profile=profile)

@app.route("/certifications")
def certifications():
    return render_template("certifications.html", profile=profile)

@app.route("/resume")
def resume_page():
    return render_template("resume.html", profile=profile)

@app.route("/animations")
def animations_page():
    return render_template("animations.html", profile=profile)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        flash("Thanks for reaching out! I'll get back to you soon.", "success")
    return render_template("contact.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)
