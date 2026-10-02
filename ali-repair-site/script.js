const header = document.querySelector('.site-header');
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
const navLinks = document.querySelectorAll('.main-nav a');
const form = document.querySelector('#contact-form');
const formNote = document.querySelector('#form-note');

const updateHeader = () => {
  header.classList.toggle('is-scrolled', window.scrollY > 10);
};

updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuToggle?.addEventListener('click', () => {
  const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!isOpen));
  menuToggle.classList.toggle('is-open', !isOpen);
  nav.classList.toggle('is-open', !isOpen);
});

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.classList.remove('is-open');
    nav.classList.remove('is-open');
  });
});

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  const fields = [...form.querySelectorAll('[required]')];
  const valid = fields.every((field) => field.value.trim());

  if (!valid) {
    formNote.textContent = 'لطفاً نام، شماره تماس و توضیح مشکل دستگاه را کامل کنید.';
    formNote.classList.remove('is-submitted');
    const firstEmpty = fields.find((field) => !field.value.trim());
    firstEmpty?.focus();
    return;
  }

  formNote.textContent = 'درخواست شما آماده است. برای ارسال واقعی، شماره تماس یا واتساپ فروشگاه را به این فرم متصل کنید.';
  formNote.classList.add('is-submitted');
});

const revealItems = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}

document.querySelector('#year').textContent = new Intl.DateTimeFormat('fa-IR', {
  year: 'numeric'
}).format(new Date());
