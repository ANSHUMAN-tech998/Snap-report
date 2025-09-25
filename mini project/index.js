const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

// Switch to Register form
if (registerLink && wrapper) {
  registerLink.addEventListener('click', (e) => {
    e.preventDefault();
    wrapper.classList.add('active');
  });
}

// Switch back to Login form
if (loginLink && wrapper) {
  loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    wrapper.classList.remove('active');
  });
}

// Optional: Open popup (only if popup trigger exists on the page)
if (btnPopup && wrapper) {
  btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
  });
}

// Optional: Close popup (only if close icon exists on the page)
if (iconClose && wrapper) {
  iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
  });
}

// Handle Login form submit -> redirect to home
const loginForm = document.querySelector('.form-box.login form');
if (loginForm) {
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    // TODO: perform real authentication here
    window.location.href = 'index.html';
  });
}

// Handle Register form submit -> redirect to home
const registerForm = document.querySelector('.form-box.register form');
if (registerForm) {
  registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    // TODO: perform real registration here
    window.location.href = 'index.html';
  });
}