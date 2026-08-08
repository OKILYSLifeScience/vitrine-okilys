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

// Scrollspy : surligne l'entrée de menu correspondant à la section visible
const spyLinks = [...document.querySelectorAll('.nav a[href^="#"]:not(.nav__cta)')].filter(a => a.getAttribute('href').length > 1);
const spySections = [...document.querySelectorAll('main section[id]')];

if (spyLinks.length && spySections.length) {
  const updateSpy = () => {
    const pos = window.scrollY + 160;
    let currentId = null;
    for (const s of spySections) {
      if (s.offsetTop <= pos) currentId = s.id;
    }
    spyLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + currentId));
  };
  window.addEventListener('scroll', updateSpy, { passive: true });
  updateSpy();
}

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Contact form -> Web3Forms (relais d'envoi pour site statique, sans backend)
const form = document.getElementById('contact-form');
const note = document.getElementById('form-note');
const isEnglish = document.documentElement.lang === 'en';
const formMsg = isEnglish
  ? {
      sending: 'Sending…',
      sent: 'Message sent, thank you! I will get back to you shortly.',
      failed: 'Sending failed. Please try again or email me directly (address opposite).',
      network: 'Sending failed (connection issue). Please try again or email me directly (address opposite).'
    }
  : {
      sending: 'Envoi en cours…',
      sent: 'Message envoyé, merci ! Je reviens vers vous rapidement.',
      failed: "L'envoi a échoué. Vous pouvez réessayer ou m'écrire directement par email (adresse ci-contre).",
      network: "L'envoi a échoué (connexion). Vous pouvez réessayer ou m'écrire directement par email (adresse ci-contre)."
    };

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('contact-submit');
    submitBtn.disabled = true;
    note.textContent = formMsg.sending;

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      });
      const result = await response.json();
      if (result.success) {
        form.reset();
        note.textContent = formMsg.sent;
      } else {
        note.textContent = formMsg.failed;
      }
    } catch (err) {
      note.textContent = formMsg.network;
    } finally {
      submitBtn.disabled = false;
    }
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
