#!/usr/bin/env python3
"""Generate pure static HTML files from profile.json. No Jinja, no Flask."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "profile.json"), "r", encoding="utf-8") as f:
    p = json.load(f)

# ------------------------------------------------------------------ helpers

def head(title):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="static/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>'''


def nav(page):
    """page is the current filename, e.g. 'index.html'."""
    links = [
        ("index.html", "Home"),
        ("about.html", "About"),
        ("projects.html", "Projects"),
        ("resume.html", "Resume"),
        ("contact.html", "Contact"),
    ]
    items = ""
    for href, label in links:
        cls = ' class="active"' if page == href else ""
        items += f'        <li><a href="{href}"{cls}>{label}</a></li>\n'
    return f'''<nav>
    <a href="index.html" class="nav-brand">{p['name'].split()[-1][:2].upper()}</a>
    <div class="nav-right">
      <ul class="nav-links">
{items}      </ul>
      <div class="nav-socials">
        <a href="{p['social']['github']}" class="nav-social" target="_blank"><i class="fab fa-github"></i></a>
        <a href="{p['social']['linkedin']}" class="nav-social" target="_blank"><i class="fab fa-linkedin"></i></a>
        <button class="mobile-menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('mobile-open')" aria-label="Menu">☰</button>
      </div>
    </div>
  </nav>'''


def footer():
    return f'''<footer>
    <p>Designed & Built by <span>{p['name']}</span> &copy; 2026 &nbsp;|&nbsp; {p['title']}</p>
  </footer>
  <script src="static/js/main.js"></script>'''


def page(title, filename, body):
    return f"""{head(title)}
<body>
  {nav(filename)}

  <main>
{body}
  </main>

  {footer()}
</body>
</html>"""


# ------------------------------------------------------------------ pages

# ---------- HOME ----------
featured = p.get("projects", [])[:3]

featured_cards = "\n    ".join(
    f'''<div class="card fade-in">
      <span class="card-icon">{proj.get('icon', '🚀')}</span>
      <h3>{proj['name']}</h3>
      <p>{proj['description']}</p>
      <div class="card-tags">
        {''.join(f'<span class="tag">{tag}</span>' for tag in proj.get('tags', []))}
      </div>
      <a href="projects.html" class="card-link">View Details →</a>
    </div>'''
    for proj in featured
)

skills_grid = "\n    ".join(
    f'''<div class="skill-group fade-in">
      <h3>{cat}</h3>
      <ul class="skill-list">
        {''.join(f'<li>{item}</li>' for item in items)}
      </ul>
    </div>'''
    for cat, items in p["skills"].items()
)

if p.get("certifications"):
    certs_html = "\n    ".join(
        f'''<div class="cert-badge fade-in">
      <span class="cert-icon">🏅</span>
      <div>
        <h4>{cert['name']}</h4>
        <p>{cert['issuer']}</p>
      </div>
    </div>'''
        for cert in p["certifications"]
    )
else:
    certs_html = '''<div class="cert-badge fade-in">
      <span class="cert-icon">📜</span>
      <div>
        <h4>Certifications Coming Soon</h4>
        <p>Pursuing AWS, GCP & Kubernetes certs</p>
      </div>
    </div>'''

home_body = f'''<div class="hero">
    <p class="hero-tag fade-in">Hello, I am</p>
    <h1 class="fade-in">{p['name'].split()[0]}<br>{' '.join(p['name'].split()[1:])}</h1>
    <h2 class="fade-in">{p['title']}</h2>
    <p class="fade-in">{p['tagline']}</p>

    <div class="btn-group fade-in">
      <a href="projects.html" class="btn btn-primary">View My Work</a>
      <a href="contact.html" class="btn btn-outline">Contact Me</a>
    </div>

    <div class="stats fade-in">
      <div class="stat-item"><span class="stat-number">{p['stats']['weeks_training']}</span><span class="stat-label">Weeks of Training</span></div>
      <div class="stat-item"><span class="stat-number">{p['stats']['projects_delivered']}+</span><span class="stat-label">Projects Delivered</span></div>
      <div class="stat-item"><span class="stat-number">{p['stats']['cloud_platforms']}</span><span class="stat-label">Cloud Platforms</span></div>
      <div class="stat-item"><span class="stat-number">{p['stats']['certifications']}</span><span class="stat-label">GCP Certification</span></div>
    </div>
  </div>

  <section>
    <h2 class="section-title fade-in">What I Work <span>With</span></h2>
    <div class="section-line fade-in"></div>
    <div class="skills-grid">
    {skills_grid}
    </div>
  </section>

  <section>
    <h2 class="section-title fade-in">Featured <span>Projects</span></h2>
    <div class="section-line fade-in"></div>
    <div class="card-grid">
    {featured_cards}
    </div>
    <div style="text-align:center;margin-top:2.5rem;">
      <a href="projects.html" class="btn btn-outline">See All Projects</a>
    </div>
  </section>

  <section>
    <h2 class="section-title fade-in">Certifications</h2>
    <div class="section-line fade-in"></div>
    <div class="cert-grid">
    {certs_html}
    </div>
  </section>'''

# ---------- ABOUT ----------
available = "\n        ".join(
    f'<li><span>➜</span> {role}</li>' for role in p.get("available_for", [])
)

about_body = f'''<section>
    <div class="page-hero">
      <h1 class="fade-in">About <span>Me</span></h1>
      <p class="fade-in">{p['title']} · {p['location']}</p>
    </div>
    <div class="about-grid" style="padding-top:40px;">
      <div class="about-text fade-in">
        <p><span>{p['name']}</span> — {p['about']}</p>
        <h3 style="color:var(--gold);margin:1.5rem 0 0.8rem;">Available For</h3>
        <ul class="values-list">
        {available}
        </ul>
        <div class="btn-group" style="margin-top:1.5rem;">
          <a href="resume.html" class="btn btn-primary">View Resume</a>
          <a href="contact.html" class="btn btn-outline">Contact Me</a>
        </div>
      </div>
      <div class="fade-in">
        <div style="background:var(--navy-card);border:1px solid var(--gold-glow);border-radius:10px;padding:2rem;">
          <h3 style="color:var(--gold);margin-bottom:1rem;">Core Skills</h3>
          <ul class="values-list">
            <li><span>☁️</span> AWS, Azure, GCP, Linux</li>
            <li><span>🐳</span> Docker, Kubernetes, Helm</li>
            <li><span>🏗️</span> Terraform, Ansible, Pulumi</li>
            <li><span>⚙️</span> Jenkins, GitHub Actions, ArgoCD</li>
            <li><span>📊</span> Prometheus, Grafana, ELK</li>
            <li><span>🤖</span> Claude Code, GitHub Copilot</li>
          </ul>
        </div>
      </div>
    </div>
  </section>'''

# ---------- PROJECTS ----------
project_cards = "\n    ".join(
    f'''<div class="card fade-in">
      <span class="card-icon">{proj.get('icon', '🚀')}</span>
      <h3>{proj['name']}</h3>
      <p>{proj['description']}</p>
      <div class="card-tags">
        {''.join(f'<span class="tag">{tag}</span>' for tag in proj.get('tags', []))}
      </div>
      <div class="card-tags" style="margin-top:0.8rem;">
        {f'<a href="{proj["github"]}" class="btn btn-sm btn-primary" target="_blank">Code</a>' if proj.get('github') else ''}
        {f'<a href="{proj["demo"]}" class="btn btn-sm btn-outline" target="_blank">Demo</a>' if proj.get('demo') else ''}
      </div>
    </div>'''
    for proj in p.get("projects", [])
)

projects_body = f'''<section>
    <div class="page-hero">
      <h1 class="fade-in">Featured <span>Projects</span></h1>
      <p class="fade-in">DevOps, Cloud, and Infrastructure projects I've built.</p>
    </div>
    <div style="text-align:center;margin-bottom:2rem;" class="fade-in">
      <a href="{p['social']['github']}" class="btn btn-primary" target="_blank"><i class="fab fa-github"></i> GitHub Profile</a>
    </div>
    <div class="card-grid">
    {project_cards}
    </div>
  </section>'''

# ---------- RESUME ----------
skill_groups = "\n    ".join(
    f'''<div class="skill-group">
      <h3>{cat}</h3>
      <ul class="skill-list">
        {''.join(f'<li>{item}</li>' for item in items)}
      </ul>
    </div>'''
    for cat, items in p["skills"].items()
)

exp_items = "\n    ".join(
    f'''<div style="margin-bottom:1.5rem;">
      <strong style="color:var(--white);">{job['title']}</strong>
      <p style="color:var(--grey);font-size:0.9rem;">{job['company']} · {job['dates']}</p>
      <p style="color:var(--grey);">{job['description']}</p>
    </div>'''
    for job in p.get("experience", [])
)
if not p.get("experience"):
    exp_items = '<p style="color:var(--grey);">Experience details coming soon.</p>'

proj_items = "\n    ".join(
    f'''<div style="margin-bottom:1rem;">
      <strong style="color:var(--white);">{proj['name']}</strong>
      <p style="color:var(--grey);">{proj['description']}</p>
    </div>'''
    for proj in p.get("projects", [])
)

cert_list = "\n    ".join(
    f'<li>{cert["name"]} — {cert["issuer"]}</li>'
    for cert in p.get("certifications", [])
)
if cert_list:
    cert_html = f'<ul style="color:var(--grey);">\n    {cert_list}\n    </ul>'
else:
    cert_html = '<p style="color:var(--grey);">Certifications coming soon.</p>'

resume_body = f'''<section>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;">
      <h1 class="page-hero" style="padding:120px 0 0;text-align:left;"><span style="color:var(--white);font-weight:800;">Resume</span></h1>
      <button class="btn btn-primary" onclick="window.print()">🖨 Print</button>
    </div>
    <div class="fade-in" style="margin-bottom:2rem;">
      <h2 style="color:var(--gold);font-size:1.5rem;">{p['name']}</h2>
      <p style="color:var(--grey);">{p['title']} · {p['location']}</p>
      <p style="color:var(--grey);"><i class="fas fa-envelope"></i> {p['email']}</p>
    </div>
    <div class="fade-in" style="margin-bottom:2rem;">
      <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Summary</h3>
      <p style="color:var(--grey);">{p['about']}</p>
    </div>
    <div class="fade-in" style="margin-bottom:2rem;">
      <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Skills</h3>
      <div class="skills-grid">
    {skill_groups}
      </div>
    </div>
    <div class="fade-in" style="margin-bottom:2rem;">
      <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Experience</h3>
    {exp_items}
    </div>
    <div class="fade-in" style="margin-bottom:2rem;">
      <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Projects</h3>
    {proj_items}
    </div>
    <div class="fade-in">
      <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Certifications</h3>
    {cert_html}
    </div>
  </section>
  <style>
    @media print {{ nav, footer, .btn {{ display:none !important; }} body {{ color:#000; background:#fff; }} .card, .skill-group, .cert-badge {{ border-color:#ddd; }} }}
  </style>'''

# ---------- CONTACT ----------
contact_body = f'''<section>
    <div class="page-hero">
      <h1 class="fade-in">Let's <span>Connect</span></h1>
      <p class="fade-in">Open to DevOps roles, internships, and collaborations.</p>
    </div>
    <div class="contact-grid" style="padding-top:40px;">
      <div class="fade-in">
        <div style="background:var(--navy-card);border:1px solid var(--gold-glow);border-radius:10px;padding:2rem;">
          <h3 style="color:var(--gold);margin-bottom:1rem;">Reach Out</h3>
          <div class="contact-item">
            <span class="contact-icon">📧</span>
            <a href="mailto:{p['email']}">{p['email']}</a>
          </div>
          <div class="contact-item">
            <span class="contact-icon">📍</span>
            <span>{p['location']}</span>
          </div>
          <div class="social-links">
            <a href="{p['social']['github']}" target="_blank"><i class="fab fa-github"></i> GitHub</a>
            <a href="{p['social']['linkedin']}" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
            <a href="{p['social']['hashnode']}" target="_blank"><i class="fas fa-blog"></i> Hashnode</a>
            <a href="{p['social']['medium']}" target="_blank"><i class="fab fa-medium"></i> Medium</a>
          </div>
        </div>
      </div>
      <div class="fade-in">
        <div style="background:var(--navy-card);border:1px solid var(--gold-glow);border-radius:10px;padding:2rem;">
          <h3 style="color:var(--gold);margin-bottom:1rem;">Send a Message</h3>
          <form name="contact" data-netlify="true">
            <div class="form-group">
              <label class="form-label">Name</label>
              <input type="text" class="form-control" name="name" required>
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input type="email" class="form-control" name="email" required>
            </div>
            <div class="form-group">
              <label class="form-label">Subject</label>
              <input type="text" class="form-control" name="subject" required>
            </div>
            <div class="form-group">
              <label class="form-label">Message</label>
              <textarea class="form-control" name="message" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary w-100">Send Message</button>
          </form>
        </div>
      </div>
    </div>
  </section>'''

# ------------------------------------------------------------------ write

pages = [
    ("index.html", f"{p['name']} — {p['title']}", home_body),
    ("about.html", f"About — {p['name']}", about_body),
    ("projects.html", f"Projects — {p['name']}", projects_body),
    ("resume.html", f"Resume — {p['name']}", resume_body),
    ("contact.html", f"Contact — {p['name']}", contact_body),
]

for filename, title, body in pages:
    path = os.path.join(BASE, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page(title, filename, body))
    print(f"Generated {filename}")

print("All static files generated.")
