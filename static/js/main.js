document.addEventListener('DOMContentLoaded', function() {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Close mobile menu if open
        const navLinks = document.getElementById('navLinks');
        if (navLinks) navLinks.classList.remove('mobile-open');
      }
    });
  });

  // Active nav link based on scroll position
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  function updateActiveNav() {
    let current = '';
    const scrollPos = window.scrollY + 100;

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        current = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.style.color = '';
      const href = link.getAttribute('href');
      if (href === '#' + current) {
        link.style.color = 'var(--gold)';
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav);
  updateActiveNav();

  // Scroll reveal for fade-up elements
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        entry.target.style.opacity = '1';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-up, .fade-up-2, .fade-up-3').forEach(el => observer.observe(el));

  // Image modal (certificates + project screenshots)
  const certModal = document.getElementById('certModal');
  const certModalImg = document.getElementById('certModalImg');
  const certModalClose = certModal ? certModal.querySelector('.cert-modal-close') : null;
  const certModalBackdrop = certModal ? certModal.querySelector('.cert-modal-backdrop') : null;

  function openImageModal(imageSrc, altText) {
    if (!certModal || !certModalImg) return;
    certModalImg.src = imageSrc;
    certModalImg.alt = altText || 'Image preview';
    certModal.classList.add('active');
    certModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeImageModal() {
    if (!certModal) return;
    certModal.classList.remove('active');
    certModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    certModalImg.src = '';
    certModalImg.alt = '';
  }

  document.querySelectorAll('.cert-card-clickable').forEach(card => {
    card.addEventListener('click', function(e) {
      // Don't trigger if the user is selecting text
      if (window.getSelection().toString().length > 0) return;
      const imageSrc = this.getAttribute('data-image');
      const altText = this.querySelector('.cert-name')?.textContent || 'Certificate preview';
      if (imageSrc) {
        e.preventDefault();
        openImageModal(imageSrc, altText);
      }
    });
  });

  document.querySelectorAll('.project-image').forEach(img => {
    img.addEventListener('click', function(e) {
      e.preventDefault();
      openImageModal(this.src, this.alt);
    });
  });

  if (certModalClose) {
    certModalClose.addEventListener('click', closeImageModal);
  }

  if (certModalBackdrop) {
    certModalBackdrop.addEventListener('click', closeImageModal);
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && certModal && certModal.classList.contains('active')) {
      closeImageModal();
    }
  });
});
