from flask import Flask, render_template, request, flash
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

with open(os.path.join(os.path.dirname(__file__), "profile.json"), "r") as f:
    profile = json.load(f)

@app.route("/")
def home():
    featured_projects = profile.get("projects", [])[:3]
    return render_template("home.html", profile=profile, featured_projects=featured_projects)

@app.route("/about")
def about():
    return render_template("about.html", profile=profile)

@app.route("/projects")
def projects_page():
    return render_template("projects.html", profile=profile)

@app.route("/resume")
def resume_page():
    return render_template("resume.html", profile=profile)

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
