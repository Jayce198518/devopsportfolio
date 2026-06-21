"""Build static site using Jinja2 (no Flask/Frozen-Flask required)."""
import json
import os
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

def build():
    clean_build()
    copy_static()

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    def url_for(endpoint, filename=None):
        if filename:
            return "static/" + filename
        mapping = {"home": "index", "about": "about", "projects_page": "projects", "resume_page": "resume", "contact": "contact"}
        return mapping.get(endpoint, endpoint) + ".html"
    env.globals["url_for"] = url_for
    env.globals["get_flashed_messages"] = lambda with_categories=False: []
    env.globals["request"] = type("Request", (), {"method": "GET", "form": {}})()

    with open(os.path.join(BASE_DIR, "profile.json"), "r") as f:
        profile = json.load(f)

    featured_projects = profile.get("projects", [])[:3]

    pages = {
        "home":     {"template": "home.html",     "output": "index.html",     "ctx": {"profile": profile, "featured_projects": featured_projects}},
        "about":    {"template": "about.html",    "output": "about.html",     "ctx": {"profile": profile}},
        "projects": {"template": "projects.html", "output": "projects.html",  "ctx": {"profile": profile}},
        "resume":   {"template": "resume.html",   "output": "resume.html",    "ctx": {"profile": profile}},
        "contact":  {"template": "contact.html",  "output": "contact.html",   "ctx": {"profile": profile}},
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
