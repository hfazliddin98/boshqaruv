// Password visibility toggle
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                togglePassword.classList.remove('bi-eye-slash');
                togglePassword.classList.add('bi-eye');
            } else {
                passwordInput.type = 'password';
                togglePassword.classList.remove('bi-eye');
                togglePassword.classList.add('bi-eye-slash');
            }
        });
    }

    // Input focus style enhancement
    $('.form-control').focus(function() {
        $(this).parent().find('label').css('color', 'var(--primary-color)');
    }).blur(function() {
        $(this).parent().find('label').css('color', '');
    });
});