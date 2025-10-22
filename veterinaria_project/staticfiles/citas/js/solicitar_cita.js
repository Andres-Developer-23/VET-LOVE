document.addEventListener('DOMContentLoaded', function() {
    const mascotaSelect = document.getElementById('id_mascota');
    const infoMascotaDiv = document.getElementById('info_mascota');
    const prioridadSelect = document.getElementById('id_prioridad');
    const sintomasField = document.getElementById('id_sintomas');
    const btnSolicitarCita = document.getElementById('btnSolicitarCita');
    const btnConfirmarCita = document.getElementById('btnConfirmarCita');
    const citaForm = document.getElementById('citaForm');
    const confirmacionModal = document.getElementById('confirmacionModal');

    // Elementos del modal
    const modalMascotaInfo = document.getElementById('modalMascotaInfo');
    const modalCitaInfo = document.getElementById('modalCitaInfo');
    const modalContactoInfo = document.getElementById('modalContactoInfo');
    const modalMotivoInfo = document.getElementById('modalMotivoInfo');

    // Datos de las mascotas (pasados desde el template)
    const mascotasData = window.mascotasData || {};

    // Opciones de tipos de consulta
    const tipoOptions = {
        'consulta_general': 'Consulta General',
        'vacunacion': 'Vacunación',
        'desparasitacion': 'Desparasitación',
        'urgencia': 'Urgencia',
        'cirugia': 'Cirugía',
        'estetica': 'Estética/Baño',
        'odontologia': 'Odontología',
        'analisis': 'Análisis Clínicos',
        'radiologia': 'Radiología',
        'ecografia': 'Ecografía',
        'control': 'Control de Peso',
        'comportamiento': 'Consulta de Comportamiento',
        'nutricion': 'Consulta Nutricional'
    };

    // Opciones de prioridad
    const prioridadOptions = {
        'normal': 'Normal',
        'urgente': 'Urgente',
        'emergencia': 'Emergencia'
    };

    function actualizarInfoMascota() {
        const mascotaId = mascotaSelect.value;

        if (mascotaId && mascotasData[mascotaId]) {
            const mascota = mascotasData[mascotaId];

            let html = `
                <div class="row">
                    <div class="col-12">
                        <h6 class="mb-2">${mascota.nombre} - ${mascota.especie}</h6>
                    </div>
                </div>
                <div class="row">
            `;

            // Información básica
            if (mascota.raza !== 'No especificada') {
                html += `<div class="col-6"><small><strong>Raza:</strong> ${mascota.raza}</small></div>`;
            }

            if (mascota.sexo !== 'No especificado') {
                html += `<div class="col-6"><small><strong>Sexo:</strong> ${mascota.sexo}</small></div>`;
            }

            // Información de edad
            let infoEdad = '';
            if (mascota.fecha_nacimiento !== 'No especificada') {
                infoEdad = `Nacimiento: ${mascota.fecha_nacimiento}`;
            } else if (mascota.edad !== 'No especificada') {
                infoEdad = `Edad: ${mascota.edad} años`;
            } else {
                infoEdad = '<span class="text-warning"><i class="fas fa-exclamation-triangle"></i> Edad no especificada</span>';
            }

            html += `<div class="col-6"><small><strong>${infoEdad}</strong></small></div>`;

            // Peso y color
            if (mascota.peso !== 'No especificado') {
                html += `<div class="col-6"><small><strong>Peso:</strong> ${mascota.peso} kg</small></div>`;
            }

            if (mascota.color !== 'No especificado') {
                html += `<div class="col-6"><small><strong>Color:</strong> ${mascota.color}</small></div>`;
            }

            html += `</div>`;

            infoMascotaDiv.innerHTML = html;

        } else {
            infoMascotaDiv.innerHTML = '<small class="text-muted">Selecciona una mascota para ver su información completa</small>';
        }
    }

    function actualizarRequerimientos() {
        if (prioridadSelect.value === 'urgente' || prioridadSelect.value === 'emergencia') {
            sintomasField.required = true;
            sintomasField.parentElement.querySelector('.form-label').innerHTML =
                'Síntomas Presentados';
            sintomasField.parentElement.querySelector('.form-text').innerHTML =
                'Para citas urgentes o de emergencia, es obligatorio describir los síntomas.';
        } else {
            sintomasField.required = false;
            sintomasField.parentElement.querySelector('.form-label').innerHTML =
                'Síntomas Presentados';
            sintomasField.parentElement.querySelector('.form-text').innerHTML =
                'Describa todos los síntomas que ha observado en su mascota.';
        }
    }

    function llenarModalConfirmacion() {
        // Obtener valores del formulario
        const mascotaId = mascotaSelect.value;
        const fecha = document.getElementById('id_fecha').value;
        const tipo = document.getElementById('id_tipo').value;
        const prioridad = document.getElementById('id_prioridad').value;
        const motivo = document.getElementById('id_motivo').value;
        const sintomas = document.getElementById('id_sintomas').value;
        const telefono = document.getElementById('id_telefono_contacto').value;
        const email = document.getElementById('id_email_contacto').value;
        const antecedentes = document.getElementById('id_antecedentes').value;
        const medicamentos = document.getElementById('id_medicamentos_actuales').value;
        const alergias = document.getElementById('id_alergias').value;

        // Información de la mascota
        if (mascotaId && mascotasData[mascotaId]) {
            const mascota = mascotasData[mascotaId];
            modalMascotaInfo.innerHTML = `
                <strong>${mascota.nombre}</strong> - ${mascota.especie}<br>
                <small>Raza: ${mascota.raza} | Edad: ${mascota.edad !== 'No especificada' ? mascota.edad + ' años' : 'No especificada'}</small><br>
                <small>Peso: ${mascota.peso} kg | Sexo: ${mascota.sexo}</small>
            `;
        } else {
            modalMascotaInfo.innerHTML = '<span class="text-danger">No se ha seleccionado una mascota</span>';
        }

        // Información de la cita
        const fechaFormateada = new Date(fecha).toLocaleString('es-ES', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        modalCitaInfo.innerHTML = `
            <strong>Fecha y Hora:</strong> ${fechaFormateada}<br>
            <strong>Tipo de Consulta:</strong> ${tipoOptions[tipo] || tipo}<br>
            <strong>Prioridad:</strong> <span class="badge bg-${prioridad === 'emergencia' ? 'danger' : prioridad === 'urgente' ? 'warning' : 'secondary'}">${prioridadOptions[prioridad] || prioridad}</span>
        `;

        // Información de contacto
        modalContactoInfo.innerHTML = `
            <strong>Teléfono:</strong> ${telefono}<br>
            <strong>Email:</strong> ${email}
        `;

        // Información del motivo y síntomas
        let motivoHTML = `<strong>Motivo:</strong> ${motivo || 'No especificado'}`;

        if (sintomas) {
            motivoHTML += `<br><strong>Síntomas:</strong> ${sintomas}`;
        }

        if (antecedentes) {
            motivoHTML += `<br><strong>Antecedentes:</strong> ${antecedentes}`;
        }

        if (medicamentos) {
            motivoHTML += `<br><strong>Medicamentos:</strong> ${medicamentos}`;
        }

        if (alergias) {
            motivoHTML += `<br><strong>Alergias:</strong> ${alergias}`;
        }

        modalMotivoInfo.innerHTML = motivoHTML;
    }

    function validarFormulario() {
        // Validaciones básicas
        const camposRequeridos = [
            'id_mascota', 'id_fecha', 'id_tipo', 'id_prioridad',
            'id_motivo', 'id_telefono_contacto', 'id_email_contacto'
        ];

        for (let campoId of camposRequeridos) {
            const campo = document.getElementById(campoId);
            if (!campo.value.trim()) {
                campo.focus();
                return false;
            }
        }

        // Validación específica para prioridades urgentes
        if ((prioridadSelect.value === 'urgente' || prioridadSelect.value === 'emergencia') &&
            !sintomasField.value.trim()) {
            sintomasField.focus();
            return false;
        }

        return true;
    }

    // Event listeners
    mascotaSelect.addEventListener('change', actualizarInfoMascota);
    prioridadSelect.addEventListener('change', actualizarRequerimientos);

    // Cuando se hace clic en "Solicitar Cita Médica"
    btnSolicitarCita.addEventListener('click', function(e) {
        e.preventDefault();
        if (validarFormulario()) {
            llenarModalConfirmacion();
            const modal = new bootstrap.Modal(confirmacionModal);
            modal.show();
        } else {
            // Evitar abrir modal; mostrar mensaje accesible
            alert('Por favor complete todos los campos obligatorios antes de solicitar la cita.');
        }
    });

    // Cuando se confirma la cita en el modal
    btnConfirmarCita.addEventListener('click', function() {
        // Mostrar loading
        btnConfirmarCita.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Confirmando...';
        btnConfirmarCita.disabled = true;

        // Cerrar el modal
        const modal = bootstrap.Modal.getInstance(confirmacionModal);
        modal.hide();

        // Enviar el formulario
        citaForm.submit();
    });

    // Resetear el botón cuando se cierra el modal
    confirmacionModal.addEventListener('hidden.bs.modal', function () {
        btnConfirmarCita.innerHTML = '<i class="fas fa-check me-1"></i>Confirmar y Solicitar Cita';
        btnConfirmarCita.disabled = false;
    });

    // Ejecutar al cargar
    actualizarInfoMascota();
    actualizarRequerimientos();
});