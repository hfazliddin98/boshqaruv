// Parolni ko'rsatish/yashirish
document.querySelector('.toggle-password').addEventListener('click', function () {
    const passwordInput = this.closest('.input-group').querySelector('input');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
    this.classList.toggle('fa-eye');
});