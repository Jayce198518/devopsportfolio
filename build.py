"""Build static site using Jinja2 (no Flask/Frozen-Flask required)."""
import json
import os
import re
import shutil
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, "build")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

def clean_build():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

def copy_static():
    dest = os.path.join(BUILD_DIR, "static")
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, dest)

def parse_requirements():
    skills = []
    req_path = os.path.join(BASE_DIR, "static", "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("Flask") and not line.startswith("Jinja2") and not line.startswith("Werkzeug") and not line.startswith("Frozen"):
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

def build():
    clean_build()
    copy_static()

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    env.globals["url_for"] = lambda endpoint, filename=None: ("static/" + filename) if filename else endpoint + ".html"
    env.globals["get_flashed_messages"] = lambda with_categories=False: []
    env.globals["request"] = type("Request", (), {"method": "GET", "form": {}})()

    with open(os.path.join(BASE_DIR, "profile.json"), "r") as f:
        profile = json.load(f)

    skills = parse_requirements()
    featured_projects = profile.get("projects", [])[:3]
    latest_posts = profile.get("blog_posts", [])[:3]
    works = []
    for p in profile.get("projects", []):
        works.append({"type": "project", "name": p["name"], "description": p["description"], "tags": p.get("tags", []), "github": p.get("github")})

    pages = {
        "home": {"template": "home.html", "output": "index.html", "ctx": {"profile": profile, "featured_projects": featured_projects, "latest_posts": latest_posts}},
        "about": {"template": "about.html", "output": "about.html", "ctx": {"profile": profile}},
        "skills": {"template": "skills.html", "output": "skills.html", "ctx": {"profile": profile, "skills": skills}},
        "experience": {"template": "experience.html", "output": "experience.html", "ctx": {"profile": profile}},
        "portfolio": {"template": "portfolio.html", "output": "portfolio.html", "ctx": {"profile": profile, "works": works}},
        "projects": {"template": "projects.html", "output": "projects.html", "ctx": {"profile": profile}},
        "blog": {"template": "blog.html", "output": "blog.html", "ctx": {"profile": profile}},
        "certifications": {"template": "certifications.html", "output": "certifications.html", "ctx": {"profile": profile}},
        "resume": {"template": "resume.html", "output": "resume.html", "ctx": {"profile": profile}},
        "animations": {"template": "animations.html", "output": "animations.html", "ctx": {"profile": profile}},
        "contact": {"template": "contact.html", "output": "contact.html", "ctx": {"profile": profile}},
    }

    for name, page in pages.items():
        template = env.get_template(page["template"])
        html = template.render(**page["ctx"])
        with open(os.path.join(BUILD_DIR, page["output"]), "w") as f:
            f.write(html)
        print(f"Built: {page['output']}")

    print(f"\nStatic site built in {BUILD_DIR}")

if __name__ == "__main__":
    build()
