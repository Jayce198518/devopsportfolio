"""Batch write all redesigned templates."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE, "templates")

def write(name, content):
    with open(os.path.join(TEMPLATES, name), "w") as f:
        f.write(content)
    print(f"Wrote {name}")

def run():
    write("about.html", '''{% extends "base.html" %}
{% block title %}About — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">About <span>Me</span></h1>
    <p class="fade-in">{{ profile.title }} · {{ profile.location }}</p>
  </div>
  <div class="about-grid" style="padding-top:40px;">
    <div class="about-text fade-in">
      <p><span>{{ profile.name }}</span> — {{ profile.about }}</p>
      <h3 style="color:var(--gold);margin:1.5rem 0 0.8rem;">Available For</h3>
      <ul class="values-list">
        {% for role in profile.available_for %}<li><span>➜</span> {{ role }}</li>{% endfor %}
      </ul>
      <div class="btn-group" style="margin-top:1.5rem;">
        <a href="{{ url_for('resume_page') }}" class="btn btn-primary">View Resume</a>
        <a href="{{ url_for('contact') }}" class="btn btn-outline">Contact Me</a>
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
</section>
{% endblock %}''')

    write("skills.html", '''{% extends "base.html" %}
{% block title %}Skills — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Skills & <span>Tools</span></h1>
    <p class="fade-in">Years of experience mapped from my personal requirements.txt</p>
  </div>
  <div class="skills-grid" style="padding-top:40px;">
    {% for skill in skills %}
    <div class="skill-group fade-in">
      <h3>{{ skill.name }}</h3>
      <ul class="skill-list">
        <li style="background:var(--gold);color:var(--navy);font-weight:600;">{{ skill.operator }}{{ skill.level }} years</li>
        {% if skill.description %}<li style="background:transparent;border:1px solid var(--gold-glow);">{{ skill.description }}</li>{% endif %}
      </ul>
    </div>
    {% endfor %}
  </div>
  <div class="fade-in" style="text-align:center;margin-top:3rem;">
    <a href="{{ profile.social.github }}" class="btn btn-primary" target="_blank"><i class="fab fa-github"></i> View GitHub</a>
  </div>
</section>
{% endblock %}''')

    write("experience.html", '''{% extends "base.html" %}
{% block title %}Experience — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Work <span>Experience</span></h1>
    <p class="fade-in">My professional journey in DevOps and Cloud Engineering.</p>
  </div>
  <div class="timeline" style="padding-top:40px;">
    {% for job in profile.experience %}
    <div class="timeline-item fade-in">
      <div class="timeline-date">{{ job.dates }}</div>
      <div class="timeline-title">{{ job.title }}</div>
      <div class="timeline-org">{{ job.company }} · {{ job.location or '' }}</div>
      <div class="timeline-desc">{{ job.description }}</div>
      {% if job.achievements %}
      <ul style="color:var(--grey);margin-top:0.5rem;padding-left:1.2rem;">
        {% for ach in job.achievements %}<li>{{ ach }}</li>{% endfor %}
      </ul>
      {% endif %}
    </div>
    {% else %}
    <div class="text-center py-5 fade-in">
      <p style="color:var(--grey);font-size:1.2rem;">Experience details coming soon.</p>
      <a href="{{ url_for('projects_page') }}" class="btn btn-primary mt-3">View Projects</a>
    </div>
    {% endfor %}
  </div>
</section>
{% endblock %}''')

    write("portfolio.html", '''{% extends "base.html" %}
{% block title %}Portfolio — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">My <span>Portfolio</span></h1>
    <p class="fade-in">A combined gallery of projects and professional experience.</p>
  </div>
  <div class="card-grid" style="padding-top:40px;">
    {% for work in works %}
    <div class="card fade-in">
      <span class="tag" style="margin-bottom:0.8rem;display:inline-block;">{{ work.type | title }}</span>
      <h3>{{ work.name }}</h3>
      <p>{{ work.description }}</p>
      {% if work.tags %}
      <div class="card-tags">
        {% for tag in work.tags %}<span class="tag">{{ tag }}</span>{% endfor %}
      </div>
      {% endif %}
      {% if work.github %}<a href="{{ work.github }}" class="card-link" target="_blank">View Code →</a>{% endif %}
    </div>
    {% endfor %}
  </div>
</section>
{% endblock %}''')

    write("projects.html", '''{% extends "base.html" %}
{% block title %}Projects — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Featured <span>Projects</span></h1>
    <p class="fade-in">DevOps, Cloud, and Infrastructure projects I've built.</p>
  </div>
  <div style="text-align:center;margin-bottom:2rem;" class="fade-in">
    <a href="{{ profile.social.github }}" class="btn btn-primary" target="_blank"><i class="fab fa-github"></i> GitHub Profile</a>
  </div>
  <div class="card-grid">
    {% for project in profile.projects %}
    <div class="card fade-in">
      <h3>{{ project.name }}</h3>
      <p>{{ project.description }}</p>
      <div class="card-tags">{% for tag in project.tags %}<span class="tag">{{ tag }}</span>{% endfor %}</div>
      <div class="card-tags" style="margin-top:0.8rem;">
        {% if project.github %}<a href="{{ project.github }}" class="btn btn-sm btn-primary" target="_blank">Code</a>{% endif %}
        {% if project.demo %}<a href="{{ project.demo }}" class="btn btn-sm btn-outline" target="_blank">Demo</a>{% endif %}
      </div>
    </div>
    {% endfor %}
  </div>
</section>
{% endblock %}''')

    write("blog.html", '''{% extends "base.html" %}
{% block title %}Blog — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Blog & <span>Articles</span></h1>
    <p class="fade-in">Thoughts on DevOps, Cloud, and Infrastructure.</p>
  </div>
  <div style="text-align:center;margin-bottom:2rem;" class="fade-in">
    <a href="{{ profile.social.hashnode }}" class="btn btn-primary" target="_blank">Hashnode</a>
    <a href="{{ profile.social.medium }}" class="btn btn-outline" target="_blank">Medium</a>
  </div>
  <div class="card-grid">
    {% for post in profile.blog_posts %}
    <div class="card fade-in">
      <span class="tag">Hashnode</span>
      <h3>{{ post.title }}</h3>
      <p>{{ post.excerpt }}</p>
      <a href="{{ post.url }}" class="card-link" target="_blank">Read Article →</a>
    </div>
    {% endfor %}
  </div>
</section>
{% endblock %}''')

    write("certifications.html", '''{% extends "base.html" %}
{% block title %}Certifications — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Certifications</h1>
    <p class="fade-in">Credentials and recognitions earned along the journey.</p>
  </div>
  <div class="cert-grid" style="padding-top:40px;">
    {% if profile.certifications %}
      {% for cert in profile.certifications %}
      <div class="cert-badge fade-in">
        <span class="cert-icon">🏅</span>
        <div>
          <h4>{{ cert.name }}</h4>
          <p>{{ cert.issuer }} · {{ cert.date_earned }}</p>
        </div>
      </div>
      {% endfor %}
    {% else %}
    <div class="cert-badge fade-in">
      <span class="cert-icon">📜</span>
      <div>
        <h4>Certifications Coming Soon</h4>
        <p>Pursuing AWS, GCP, Kubernetes & more</p>
      </div>
    </div>
    {% endif %}
  </div>
  <div style="text-align:center;margin-top:2rem;" class="fade-in">
    <a href="{{ url_for('skills_page') }}" class="btn btn-primary">View My Skills</a>
  </div>
</section>
{% endblock %}''')

    write("resume.html", '''{% extends "base.html" %}
{% block title %}Resume — {{ profile.name }}{% endblock %}
{% block extra_css %}
<style>@media print { nav, footer, .btn { display:none !important; } body { color:#000; background:#fff; } .card, .skill-group, .cert-badge { border-color:#ddd; } }</style>
{% endblock %}
{% block content %}
<section>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;">
    <h1 class="page-hero" style="padding:120px 0 0;text-align:left;"><span style="color:var(--white);font-weight:800;">Resume</span></h1>
    <button class="btn btn-primary" onclick="window.print()">🖨 Print</button>
  </div>
  <div class="fade-in" style="margin-bottom:2rem;">
    <h2 style="color:var(--gold);font-size:1.5rem;">{{ profile.name }}</h2>
    <p style="color:var(--grey);">{{ profile.title }} · {{ profile.location }}</p>
    <p style="color:var(--grey);"><i class="fas fa-envelope"></i> {{ profile.email }}</p>
  </div>
  <div class="fade-in" style="margin-bottom:2rem;">
    <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Summary</h3>
    <p style="color:var(--grey);">{{ profile.about }}</p>
  </div>
  <div class="fade-in" style="margin-bottom:2rem;">
    <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Skills</h3>
    <div class="skills-grid">
      {% for category, items in profile.skills.items() %}
      <div class="skill-group">
        <h3>{{ category }}</h3>
        <ul class="skill-list">{% for item in items %}<li>{{ item }}</li>{% endfor %}</ul>
      </div>
      {% endfor %}
    </div>
  </div>
  <div class="fade-in" style="margin-bottom:2rem;">
    <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Experience</h3>
    {% for job in profile.experience %}
    <div style="margin-bottom:1.5rem;">
      <strong style="color:var(--white);">{{ job.title }}</strong>
      <p style="color:var(--grey);font-size:0.9rem;">{{ job.company }} · {{ job.dates }}</p>
      <p style="color:var(--grey);">{{ job.description }}</p>
    </div>
    {% else %}
    <p style="color:var(--grey);">Experience details coming soon.</p>
    {% endfor %}
  </div>
  <div class="fade-in" style="margin-bottom:2rem;">
    <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Projects</h3>
    {% for project in profile.projects %}
    <div style="margin-bottom:1rem;">
      <strong style="color:var(--white);">{{ project.name }}</strong>
      <p style="color:var(--grey);">{{ project.description }}</p>
    </div>
    {% endfor %}
  </div>
  <div class="fade-in">
    <h3 style="color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:0.5rem;margin-bottom:1rem;">Certifications</h3>
    {% if profile.certifications %}
    <ul style="color:var(--grey);">{% for cert in profile.certifications %}<li>{{ cert.name }} — {{ cert.issuer }}</li>{% endfor %}</ul>
    {% else %}
    <p style="color:var(--grey);">Certifications coming soon.</p>
    {% endif %}
  </div>
</section>
{% endblock %}''')

    write("animations.html", '''{% extends "base.html" %}
{% block title %}Animations — {{ profile.name }}{% endblock %}
{% block content %}
<section>
  <div class="page-hero">
    <h1 class="fade-in">Animations <span>Showcase</span></h1>
    <p class="fade-in">Interactive demos of DevOps workflows.</p>
  </div>
  <div class="card-grid" style="padding-top:40px;">
    <div class="card fade-in">
      <h3><i class="fas fa-terminal"></i> Terminal Typing</h3>
      <div class="terminal-window" style="margin-top:1rem;">
        <div class="terminal-header"><span class="terminal-dot red"></span><span class="terminal-dot yellow"></span><span class="terminal-dot green"></span></div>
        <div class="terminal-content" id="terminal-text"></div>
      </div>
    </div>
    <div class="card fade-in">
      <h3><i class="fas fa-stream"></i> CI/CD Pipeline</h3>
      <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;padding:2rem 0;">
        <div class="pipeline-stage" id="st1">Commit</div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-stage" id="st2">Build</div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-stage" id="st3">Test</div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-stage" id="st4">Deploy</div>
      </div>
      <div style="text-align:center;margin-top:1rem;">
        <button class="btn btn-primary" onclick="runPipeline()">Run Pipeline</button>
      </div>
    </div>
    <div class="card fade-in">
      <h3><i class="fas fa-cubes"></i> Kubernetes Pods</h3>
      <div style="text-align:center;padding:2rem 0;">
        <div style="display:inline-flex;align-items:center;gap:1.5rem;">
          <div class="pipeline-stage" style="width:100px;height:100px;"><i class="fas fa-server fa-lg"></i><br><small>Master</small></div>
          <div style="display:flex;flex-direction:column;gap:0.5rem;" id="k8s-pods">
            <div class="pipeline-stage" style="width:50px;height:50px;font-size:0.7rem;opacity:0.3;"><i class="fas fa-cube"></i></div>
            <div class="pipeline-stage" style="width:50px;height:50px;font-size:0.7rem;opacity:0.3;"><i class="fas fa-cube"></i></div>
            <div class="pipeline-stage" style="width:50px;height:50px;font-size:0.7rem;opacity:0.3;"><i class="fas fa-cube"></i></div>
          </div>
        </div>
      </div>
      <div style="text-align:center;margin-top:1rem;">
        <button class="btn btn-primary" onclick="spinUpPods()">Spin Up Pods</button>
      </div>
    </div>
  </div>
</section>
{% endblock %}
{% block extra_js %}
<script>
const cmdList = ["$ kubectl apply -f deployment.yaml","deployment.apps/web-app configured","$ helm upgrade --install myapp ./chart","Release 'myapp' upgraded","$ terraform apply -auto-approve","Apply complete! Resources: 4 added, 2 changed, 0 destroyed."];
let ci=0, ch=0; const term=document.getElementById('terminal-text');
function typeTerm(){if(ci>=cmdList.length){ci=0;term.textContent='';setTimeout(typeTerm,2000);return;} const c=cmdList[ci]; if(ch<c.length){term.textContent+=c[ch];ch++;setTimeout(typeTerm,50+Math.random()*50);}else{term.textContent+='\\n';ch=0;ci++;setTimeout(typeTerm,400);}}
if(term)typeTerm();
function runPipeline(){['st1','st2','st3','st4'].forEach((id,i)=>{setTimeout(()=>{const el=document.getElementById(id);el.style.background='var(--gold)';el.style.color='var(--navy)';el.style.transform='scale(1.2)';setTimeout(()=>el.style.transform='scale(1)',300);},i*800);}); setTimeout(()=>{['st1','st2','st3','st4'].forEach(id=>{const el=document.getElementById(id);el.style.background='var(--navy-card)';el.style.color='var(--gold)';});},4200);}
function spinUpPods(){document.querySelectorAll('#k8s-pods .pipeline-stage').forEach((p,i)=>{p.style.opacity='0.3';p.style.transform='scale(0.5)';setTimeout(()=>{p.style.transition='all 0.5s';p.style.opacity='1';p.style.transform='scale(1)';},i*600);});}
</script>
{% endblock %}''')

    write("contact.html", '''{% extends "base.html" %}
{% block title %}Contact — {{ profile.name }}{% endblock %}
{% block content %}
<section>
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
          <a href="mailto:{{ profile.email }}">{{ profile.email }}</a>
        </div>
        <div class="contact-item">
          <span class="contact-icon">📍</span>
          <span>{{ profile.location }}</span>
        </div>
        <div class="social-links">
          <a href="{{ profile.social.github }}" target="_blank"><i class="fab fa-github"></i> GitHub</a>
          <a href="{{ profile.social.linkedin }}" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>
          <a href="{{ profile.social.hashnode }}" target="_blank"><i class="fas fa-blog"></i> Hashnode</a>
          <a href="{{ profile.social.medium }}" target="_blank"><i class="fab fa-medium"></i> Medium</a>
        </div>
      </div>
    </div>
    <div class="fade-in">
      <div style="background:var(--navy-card);border:1px solid var(--gold-glow);border-radius:10px;padding:2rem;">
        <h3 style="color:var(--gold);margin-bottom:1rem;">Send a Message</h3>
        <form method="POST" action="{{ url_for('contact') }}" data-netlify="true" name="contact">
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
</section>
{% endblock %}''')

if __name__ == "__main__":
    run()
