// Contact info (email/phone) assembled at runtime from reversed strings.
// This deters basic scraping bots that read raw HTML/JS for email/phone patterns —
// it does NOT stop a headless-browser or AI crawler that fully renders the page;
// only a server-side relay can guarantee that.
function unreverse(str) { return str.split('').reverse().join(''); }

document.querySelectorAll('[data-email]').forEach((el) => {
  const email = unreverse(el.getAttribute('data-email'));
  el.setAttribute('href', 'mailto:' + email);
  if (!el.textContent.trim()) el.textContent = email;
});
document.querySelectorAll('[data-tel]').forEach((el) => {
  const tel = unreverse(el.getAttribute('data-tel'));
  const label = el.hasAttribute('data-tel-label') ? unreverse(el.getAttribute('data-tel-label')) : tel;
  el.setAttribute('href', 'tel:' + tel);
  if (!el.textContent.trim()) el.textContent = label;
});
const CONTACT_EMAIL = document.body.hasAttribute('data-contact-email')
  ? unreverse(document.body.getAttribute('data-contact-email'))
  : null;

// Mobile navigation
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
const overlay = document.getElementById('nav-overlay');

function closeNav() {
  nav.classList.remove('is-open');
  overlay.classList.remove('is-open');
  burger.classList.remove('is-open');
  burger.setAttribute('aria-expanded', 'false');
}

function toggleNav() {
  const isOpen = nav.classList.toggle('is-open');
  overlay.classList.toggle('is-open', isOpen);
  burger.classList.toggle('is-open', isOpen);
  burger.setAttribute('aria-expanded', String(isOpen));
}

if (burger) {
  burger.addEventListener('click', toggleNav);
  overlay.addEventListener('click', closeNav);
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));
}

// Sticky header shadow on scroll
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.style.boxShadow = window.scrollY > 8 ? '0 8px 24px -12px rgba(15,23,42,0.18)' : 'none';
});

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Contact form -> mailto (site statique, sans backend)
const form = document.getElementById('contact-form');
const note = document.getElementById('form-note');

if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const organisation = document.getElementById('organisation').value.trim();
    const message = document.getElementById('message').value.trim();

    const subject = encodeURIComponent(`Contact site vitrine - ${name}`);
    const body = encodeURIComponent(
      `Nom : ${name}\nEmail : ${email}\nOrganisation : ${organisation || 'Non renseignée'}\n\nMessage :\n${message}`
    );

    window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
    note.textContent = "Votre messagerie va s'ouvrir pour envoyer votre message.";
  });
}

// Accordion (FAQ / "A quoi s'attendre")
document.querySelectorAll('.accordion').forEach((accordion) => {
  accordion.querySelectorAll('.accordion__trigger').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.accordion__item');
      item.classList.toggle('is-open');
    });
  });
});
