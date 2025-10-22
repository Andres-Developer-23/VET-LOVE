// Funcionalidad para la página de login
// Mostrar/ocultar contraseña
document.addEventListener('DOMContentLoaded', function(){
  const toggle = document.getElementById('togglePassword');
  const pwdInput = document.getElementById('{{ form.password.id_for_label }}');
  function doToggle(){
    const type = pwdInput.getAttribute('type') === 'password' ? 'text' : 'password';
    pwdInput.setAttribute('type', type);
    toggle.firstElementChild.classList.toggle('fa-eye');
    toggle.firstElementChild.classList.toggle('fa-eye-slash');
    toggle.setAttribute('aria-pressed', type === 'text' ? 'true' : 'false');
  }
  if (toggle && pwdInput) {
    toggle.addEventListener('click', doToggle);
    toggle.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); doToggle(); }
    });
  }
});