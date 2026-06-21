document.addEventListener('DOMContentLoaded', function() {
  // Active nav link
  const links = document.querySelectorAll('.nav-links a');
  const path = location.pathname.replace(/\/$|\.html$/,'') || 'index';
  links.forEach(a => {
    if (a.getAttribute('href').replace(/\/$|\.html$/,'') === path) a.classList.add('active');
  });

  // Scroll reveal
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});
