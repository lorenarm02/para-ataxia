document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formregistro');
    const clave = document.getElementById('clave');
    const confirmarClave = document.getElementById('confirmar_clave');
    const error = document.getElementById('error');

    form.addEventListener('submit', function(event) {
        const password = clave.value;
        const confirmPassword = confirmarClave.value;
        const errors = [];

        // Validación de la contraseña
        if (password.length < 8) {
            errors.push('La contraseña debe tener al menos 8 caracteres.');
        }
        if (!/[A-Z]/.test(password)) {
            errors.push('La contraseña debe contener al menos una letra en mayúscula.');
        }
        if (!/[a-z]/.test(password)) {
            errors.push('La contraseña debe contener al menos una letra en minúscula.');
        }
        if (!/[0-9]/.test(password)) {
            errors.push('La contraseña debe contener al menos un número.');
        }
        if (/123456|abcdef|password/.test(password)) {
            errors.push('La contraseña no debe contener patrones comunes.');
        }

        // Validación de la confirmación de la contraseña
        if (password !== confirmPassword) {
            errors.push('Las contraseñas no coinciden.');
        }

        // Mostrar errores
        if (errors.length > 0) {
            event.preventDefault();
            error.innerHTML = errors.join('<br>');
        } else {
            error.innerHTML = '';
        }
    });

    // Validación de Bootstrap
    (function () {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms).forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

    // Validación de confirmación de contraseña en tiempo real
    function validarConfirmacionContraseña() {
        if (clave.value !== confirmarClave.value) {
            confirmarClave.setCustomValidity("Las contraseñas no coinciden");
        } else {
            confirmarClave.setCustomValidity('');
        }
    }

    clave.addEventListener('input', validarConfirmacionContraseña);
    confirmarClave.addEventListener('input', validarConfirmacionContraseña);
});

// Contar los likes
function like(idPublicacion, alreadyLiked) {
    fetch(`/like/${idPublicacion}`, {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likesSpan = document.getElementById(`likes-${idPublicacion}`);
            likesSpan.textContent = data.likes;

            const likeBtn = document.getElementById(`like-btn-${idPublicacion}`).querySelector('img');
            if (data.alreadyLiked) {
                likeBtn.src = '/static/imagenes/liked.png';
            } else {
                likeBtn.src = '/static/imagenes/like.png';
            }
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error al dar like:', error));
}

function verPassword() {
    var pass = document.getElementById("clave");
    var btn = document.getElementById("btn");
    if (pass.type === "password") {
        pass.type = "text";
        btn.src = "{{ url_for('static', filename='imagenes/nover.png') }}";
    } else {
        pass.type = "password";
        btn.src = "{{ url_for('static', filename='imagenes/ver.png') }}";
    }
}