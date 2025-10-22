// Funcionalidad para la página de login
// Mostrar/ocultar contraseña
document.addEventListener('DOMContentLoaded', function(){
  const toggle = document.getElementById('togglePassword');
  // Buscar el campo de contraseña por diferentes posibles IDs
  let pwdInput = document.getElementById('id_password') ||
                 document.getElementById('password') ||
                 document.querySelector('input[type="password"]');

  function doToggle(){
    if (!pwdInput) return;

    const type = pwdInput.getAttribute('type') === 'password' ? 'text' : 'password';
    pwdInput.setAttribute('type', type);

    // Cambiar el ícono
    const icon = toggle.querySelector('i');
    if (icon) {
      icon.classList.toggle('fa-eye');
      icon.classList.toggle('fa-eye-slash');
    }

    // Actualizar aria-pressed
    toggle.setAttribute('aria-pressed', type === 'text' ? 'true' : 'false');

    // Cambiar el aria-label
    toggle.setAttribute('aria-label', type === 'text' ? 'Ocultar contraseña' : 'Mostrar contraseña');
  }

  if (toggle && pwdInput) {
    toggle.addEventListener('click', doToggle);
    toggle.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        doToggle();
      }
    });
  } else {
    console.warn('Botón toggle o campo de contraseña no encontrados');
  }

  // Funcionalidad adicional para mejorar UX
  const form = document.querySelector('form');
  const submitBtn = document.querySelector('button[type="submit"]');

  if (form && submitBtn) {
    form.addEventListener('submit', function() {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Iniciando sesión...';
    });
  }

  // Auto-focus en el primer campo vacío
  const usernameField = document.querySelector('input[name="username"]');
  const passwordField = pwdInput;

  if (usernameField && !usernameField.value) {
    usernameField.focus();
  } else if (passwordField && !passwordField.value) {
    passwordField.focus();
  }
});