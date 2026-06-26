#!/usr/bin/env python3
"""Generate a single-page static portfolio from profile.json."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "profile.json"), "r", encoding="utf-8") as f:
    p = json.load(f)

first_name = p['name'].split()[0]
last_name = ' '.join(p['name'].split()[1:])

# ─── BUILD SECTIONS ───

# Approach (How I Work)
approach_items = "\n".join(
    f'''          <div class="step-card">
            <div class="step-num">{step['num']}</div>
            <div class="step-title">{step['title']}</div>
            <p class="step-desc">{step['description']}</p>
          </div>'''
    for step in p.get("approach", [])
)

# Projects
project_cards = "\n".join(
    f'''        <!-- {proj['name']} -->
        <div class="project-card{' featured' if proj.get('featured') else ''}">
          <div class="project-top">
            <div class="project-badges">
              {''.join(f'<span class="badge">{tag}</span>' for tag in proj.get('tags', [])[:5])}
            </div>
            <h3 class="project-title">{proj['name']}</h3>
            <p class="project-desc">{proj['description']}</p>
          </div>
          <div class="project-impact">
            <strong>Engineering Impact</strong>
            {proj.get('impact', '')}
          </div>
          <div class="project-footer">
            <div class="project-tags">
              {''.join(f'<span class="project-tag">{tag}</span>' for tag in proj.get('tags', []))}
            </div>
            {'<a href="' + proj['github'] + '" target="_blank" class="project-link">GitHub ↗</a>' if proj.get('github') else ''}
          </div>
        </div>'''
    for proj in p.get("projects", [])
)

# Skills domains
# Map emoji icons per category
skill_icons = {
    "Cloud & Infrastructure": "☁",
    "Containers & Orchestration": "🐳",
    "CI/CD & Automation": "⚙",
    "Observability & Tools": "📊",
    "Agentic AI & Emerging Tech": "🤖",
}
skill_colors = ["gold", "green", "amber", "red"]
skill_domains = "\n".join(
    f'''        <div class="domain-card">
          <div class="domain-header">
            <div class="domain-icon {skill_colors[i % len(skill_colors)]}">{skill_icons.get(cat, "🔧")}</div>
            <div class="domain-name">{cat}</div>
          </div>
          <div class="skill-pills">
            {''.join(f'<span class="skill-pill">{item}</span>' for item in items)}
          </div>
        </div>'''
    for i, (cat, items) in enumerate(p.get("skills", {}).items())
)

# Certifications
def cert_card(cert):
    border = ''
    date_style = ''
    if cert.get('current'):
        border = ' style="border-color:rgba(0,232,122,0.3)"'
        date_style = ' style="color:var(--green)"'
    elif cert.get('in_progress'):
        border = ' style="border-color:rgba(255,184,0,0.3)"'
        date_style = ' style="color:var(--amber)"'

    url = cert.get('certificate_url') or cert.get('image', '')
    img = cert.get('image', '')

    if img:
        thumb = f'''          <div class="cert-thumb">
            <img src="{img}" alt="Certificate: {cert['name']}" loading="lazy">
          </div>'''
    else:
        thumb = '''          <div class="cert-thumb cert-thumb-placeholder">
            <span>📜</span>
          </div>'''

    inner = f'''{thumb}
          <div class="cert-name">{cert['name']}</div>
          <div class="cert-date"{date_style}>{cert['issuer']} · {cert.get('date', '')}</div>
          <div class="cert-note">{cert.get('note', '')}</div>'''

    if url:
        return f'''        <a class="cert-card" href="{url}" target="_blank" rel="noopener noreferrer"{border}>
{inner}
        </a>'''
    return f'''        <div class="cert-card"{border}>
{inner}
        </div>'''

cert_cards = "\n".join(cert_card(cert) for cert in p.get("certifications", []))
# Blog articles
article_rows = "\n".join(
    f'''        <a class="article-row" href="{art['url']}" target="_blank">
          <div class="article-date">{art['date']}</div>
          <div>
            <div class="article-title">{art['title']}</div>
            <div class="article-tags">
              {''.join(f'<span class="article-tag">{tag}</span>' for tag in art.get('tags', []))}
            </div>
          </div>
          <div class="article-min">{art.get('read_time', '')}</div>
        </a>'''
    for art in p.get("blog_posts", [])
)

# Timeline
timeline_items = "\n".join(
    f'''            <div class="timeline-item">
              <div class="tl-date{' current' if item.get('current') else ''}">{item['date']}</div>
              <div>
                <div class="tl-title">{item['title']}</div>
                <div class="tl-org">{item['org']}</div>
              </div>
            </div>'''
    for item in p.get("timeline", [])
)

# Education
edu = p.get("education", [])
edu_html = ""
if edu:
    e = edu[0]
    edu_html = f"""BSc Economics<br><span style="color:var(--ghost);font-size:var(--fs-xs)">National Open University of Nigeria, 2026</span>"""

# Available for roles
roles_html = "\n".join(
    f'''              <div class="community-badge">{'⚙' if 'DevOps' in role else '☁' if 'Cloud' in role else '🏗' if 'Platform' in role else '📈'} <span>{role}</span></div>'''
    for role in p.get("available_for", [])
)

# CV certs
# CV certs
def cv_cert(cert):
    border = ''
    year_style = ''
    if cert.get('current'):
        border = ' style="border-color:rgba(0,232,122,0.3)"'
        year_style = ' style="color:var(--green)"'
    elif cert.get('in_progress'):
        border = ' style="border-color:rgba(255,184,0,0.3)"'
        year_style = ' style="color:var(--amber)"'
    return f'''          <div class="cv-cert"{border}>
            <div class="cv-cert-name">{cert['name'].replace("Google Cloud Certified — Professional Cloud Security Engineer", "Google Cloud PCSE")}</div>
            <div class="cv-cert-year"{year_style}>{cert['issuer']} · {cert.get('date', '')}</div>
          </div>'''

cv_certs = "\n".join(cv_cert(cert) for cert in p.get("certifications", []))

# Contact links
contact_links = f'''<a class="contact-link" href="{p['social']['linkedin']}" target="_blank">
              <div><span class="link-label">LinkedIn</span><span class="link-val">linkedin.com/in/jacinta-ezennajiofoeze</span></div>
            </a>
            <a class="contact-link" href="{p['social']['github']}" target="_blank">
              <div><span class="link-label">GitHub</span><span class="link-val">github.com/Jayce198518</span></div>
            </a>
            <a class="contact-link" href="{p['social']['medium']}" target="_blank">
              <div><span class="link-label">Medium</span><span class="link-val">medium.com/@jacintachinyere</span></div>
            </a>
            <a class="contact-link" href="mailto:{p['email']}">
              <div><span class="link-label">Email</span><span class="link-val">{p['email']}</span></div>
            </a>'''

# Footer social links
footer_social = f'''<a href="{p['social']['linkedin']}" target="_blank">LinkedIn</a>
        <a href="{p['social']['github']}" target="_blank">GitHub</a>
        <a href="{p['social']['medium']}" target="_blank">Medium</a>'''

# Hero certs
cert_tags = ["Google Cloud Certified — Professional Cloud Security Engineer", "Cloud Computing & Security", "On Demand IT Skills", "The CloudAdvisory — DevOps Micro Internship"]
hero_certs = "\n".join(f'            <span class="cert-tag{' active' if i < 2 else ''}">{c}</span>' for i, c in enumerate(cert_tags))

# ─── ASSEMBLE HTML ───

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['name']} | {p['title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,300;0,700;1,300&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="static/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>

  <!-- NAV -->
  <nav>
    <div class="nav-inner">
      <a class="nav-logo" href="#home">{first_name[0]}{p['name'].split()[1][0]} <span>Chinyere</span></a>
      <div class="nav-links" id="navLinks">
        <a href="#home" class="nav-item">Home</a>
        <a href="#projects" class="nav-item">Projects</a>
        <a href="#skills" class="nav-item">Skills</a>
        <a href="#blog" class="nav-item">Blog</a>
        <a href="#about" class="nav-item">About</a>
        <a href="#contact" class="nav-item">Contact</a>
        <a href="#cv" class="cv-btn">View CV</a>
        <button class="mobile-menu-btn" onclick="document.getElementById('navLinks').classList.toggle('mobile-open')" aria-label="Menu">☰</button>
      </div>
    </div>
  </nav>

  <!-- HERO -->
  <section id="home">
    <div class="grid-lines"></div>
    <div class="hero-bg"></div>
    <div class="container">
      <div class="hero-grid">
        <div class="hero-left fade-up">
          <div class="hero-tag">
            <span class="status-badge">Open to Cloud & DevOps Roles</span>
          </div>
          <h1 class="hero-name">{first_name}<br><span>{last_name}</span></h1>
          <p class="hero-role">{p['title']}</p>
          <p class="hero-desc">{p['tagline']}</p>
          <div class="hero-certs">
{hero_certs}
          </div>
          <div class="hero-btns">
            <a href="#projects" class="btn-primary">Explore Projects</a>
            <a href="#contact" class="btn-secondary">Contact Me</a>
          </div>
        </div>
        <div class="hero-right fade-up-2">
          <div class="stat-card">
            <div class="stat-num gold">{p['stats']['weeks_training']}+</div>
            <div class="stat-label">Weeks of Intensive<br>Training</div>
          </div>
          <div class="stat-card">
            <div class="stat-num gold">Google</div>
            <div class="stat-label">Cloud Certified<br>Professional 2025</div>
          </div>
          <div class="stat-card">
            <div class="stat-num amber">{p['stats']['projects_delivered']}+</div>
            <div class="stat-label">Cloud & DevOps<br>Projects Delivered</div>
          </div>
          <div class="stat-card">
            <div class="stat-num white">{p['stats']['cloud_platforms']}</div>
            <div class="stat-label">Cloud Platforms<br>Explored</div>
          </div>
        </div>
      </div>

      <hr class="divider">

      <!-- How I Work -->
      <div class="fade-up-3">
        <p class="section-label">Approach</p>
        <h2 class="section-title">How I <em>Work</em></h2>
        <div class="steps-grid">
{approach_items}
        </div>
      </div>
    </div>
  </section>

  <!-- PROJECTS -->
  <section id="projects">
    <div class="container">
      <p class="section-label">Selected Work</p>
      <h2 class="section-title">Featured <em>Projects</em></h2>
      <p style="color:var(--ghost);font-size:var(--fs-sm);margin-top:0.5rem">Cloud infrastructure, container orchestration, and automated deployment pipelines — designed, built, and documented.</p>

      <div class="projects-grid">
{project_cards}
      </div>
    </div>
  </section>

  <!-- SKILLS -->
  <section id="skills">
    <div class="container">
      <p class="section-label">Technical Stack</p>
      <h2 class="section-title">Skills & <em>Technologies</em></h2>
      <p style="color:var(--ghost);font-size:var(--fs-sm);margin-top:0.5rem">Hands-on experience across cloud platforms, containerisation, infrastructure as code, and continuous delivery — applied in real projects and professional environments.</p>

      <div class="skills-domains">
{skill_domains}
      </div>

      <p class="section-label" style="margin-top:3rem">Certifications</p>
      <div class="certs-grid">
{cert_cards}
      </div>
    </div>
  </section>

  <!-- BLOG -->
  <section id="blog">
    <div class="container">
      <p class="section-label">Writing & Research</p>
      <h2 class="section-title">Published <em>Articles</em></h2>
      <p style="color:var(--ghost);font-size:var(--fs-sm);margin-top:0.5rem">Lessons learned from real deployments, local experiments, and production missteps — written for engineers, readable by anyone.</p>

      <div class="articles-list">
{article_rows}
      </div>
      <div class="articles-cta">
        <a href="{p['social']['medium']}" target="_blank" class="view-all">View All on Medium ↗</a>
      </div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about">
    <div class="container">
      <p class="section-label">Background</p>
      <h2 class="section-title">About <em>Me</em></h2>
      <div class="about-grid">
        <div class="about-left">
          <div class="about-text">
            <p>{p['about']}</p>
            <p>My journey into tech started with intensive hands-on training at Digital Witch Support Community, where I built a solid foundation in cloud computing and security. I further honed my skills through a DevOps Micro Internship at The CloudAdvisory, working on real-world pipeline automation and cloud deployments. I am committed to continuous learning and delivering production-grade infrastructure.</p>
          </div>

          <p class="section-label" style="margin-top:2rem">Career Timeline</p>
          <div class="timeline">
{timeline_items}
          </div>
        </div>

        <div class="about-right">
          <div class="about-meta">
            <div class="meta-label">Location</div>
            <div class="meta-value">{p['location']}<br><span style="color:var(--green);font-size:var(--fs-xs)">Open to remote, hybrid, and relocation opportunities</span></div>
          </div>
          <div class="about-meta">
            <div class="meta-label">Education</div>
            <div class="meta-value">{edu_html}</div>
          </div>
          <div class="about-meta">
            <div class="meta-label">What I am Looking For</div>
            <div class="community-badges">
{roles_html}
            </div>
          </div>
          <div class="about-meta">
            <div class="meta-label">Connect</div>
            <div class="community-badges">
              <div class="community-badge">🔗 <span>GitHub</span> — github.com/Jayce198518</div>
              <div class="community-badge">💼 <span>LinkedIn</span> — linkedin.com/in/jacinta-ezennajiofoeze</div>
              <div class="community-badge">✍ <span>Medium</span> — medium.com/@jacintachinyere</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <section id="contact">
    <div class="container">
      <p class="section-label">Get in Touch</p>
      <h2 class="section-title">Let's Build Something <em>Together</em></h2>
      <div class="contact-grid">
        <div>
          <p class="contact-desc">{p['title']} · {p['location']} — if you need someone who bridges infrastructure expertise with hands-on engineering, let's talk.</p>
          <div class="contact-links">
{contact_links}
          </div>
        </div>
        <form class="contact-form" name="contact" data-netlify="true">
          <p style="display:none">
            <input name="bot-field">
          </p>
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" placeholder="Your name" required>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="your@email.com" required>
          </div>
          <div class="form-group">
            <label for="message">Message</label>
            <textarea id="message" name="message" placeholder="Tell me about the opportunity or project..." required></textarea>
          </div>
          <button type="submit" class="form-submit">Send Message →</button>
        </form>
      </div>
    </div>
  </section>

  <!-- CV -->
  <section id="cv">
    <div class="container">
      <p class="section-label">Curriculum Vitae</p>
      <h2 class="section-title">View My <em>CV</em></h2>
      <div class="cv-box">
        <div class="cv-header">
          <div class="cv-title">{p['name']} — CV</div>
          <div class="cv-btns">
            <a href="{p['social']['linkedin']}" target="_blank" class="cv-btn-li">View on LinkedIn ↗</a>
          </div>
        </div>
        <div class="cv-preview">
          <div class="icon">📄</div>
          <p>Downloadable PDF coming soon</p>
          <p style="font-size:0.7rem">For now, view full details on LinkedIn</p>
        </div>
        <div class="cv-certs">
{cv_certs}
        </div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer>
    <div class="footer-inner">
      <div class="footer-name">{p['name']}</div>
      <div class="footer-subtitle">Cloud · DevOps · Infrastructure Engineering</div>
      <div class="footer-links">
        <a href="#home">Home</a>
        <a href="#projects">Projects</a>
        <a href="#skills">Skills</a>
        <a href="#blog">Blog</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
        <a href="#cv">CV</a>
      </div>
      <div class="footer-links">
{footer_social}
      </div>
      <div class="footer-copy">© 2026 {p['name']}. All rights reserved.</div>
    </div>
  </footer>

  <script src="static/js/main.js"></script>
</body>
</html>
'''

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Generated index.html")

# Clean up any old redirect pages
for page in ["about.html", "projects.html", "resume.html", "contact.html"]:
    path = os.path.join(BASE, page)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed old {page}")

print("All done.")
