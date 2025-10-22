// Redirección automática para administradores en la página de inicio
setTimeout(function() {
    window.location.href = "{% url 'administracion:dashboard_admin' %}";
}, 2000);