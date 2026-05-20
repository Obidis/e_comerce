document.addEventListener("DOMContentLoaded", function() {
    const relojEl = document.getElementById('reloj-hora');
    const fechaEl = document.getElementById('reloj-fecha');

    if (relojEl || fechaEl) {
        function obtenerHora() {
            const fecha = new Date();

            // Hora en formato HH:MM:SS
            const horas = String(fecha.getHours()).padStart(2, '0');
            const minutos = String(fecha.getMinutes()).padStart(2, '0');
            const segundos = String(fecha.getSeconds()).padStart(2, '0');

            // Fecha en formato: Día, DD de Mes de AAAA
            const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
            const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

            const diaSemana = dias[fecha.getDay()];
            const dia = fecha.getDate();
            const mes = meses[fecha.getMonth()];
            const anio = fecha.getFullYear();

            const fechaFormateada = `${diaSemana}, ${dia} de ${mes} de ${anio}`;

            // Renderiza la hora
            if (relojEl) {
                relojEl.textContent = `${horas}:${minutos}:${segundos}`;
            }

            // Renderiza la fecha
            if (fechaEl) {
                fechaEl.textContent = fechaFormateada;
            }
        }

        // Ejecuta inmediatamente y actualiza cada segundo
        obtenerHora();
        setInterval(obtenerHora, 1000);
    }

    // Limpiar campos de login después del registro o login para evitar el autocompletado con credenciales antiguas
    const alerts = document.querySelectorAll('.alert-success');
    let shouldClear = false;
    alerts.forEach(function(alert) {
        const text = alert.textContent || '';
        if (text.includes("Usuario creado correctamente") || text.includes("Bienvenido")) {
            shouldClear = true;
        }
    });

    if (shouldClear) {
        function clearInputs() {
            const usernameInput = document.querySelector('input[name="username"]');
            const passwordInput = document.querySelector('input[name="password"]');
            if (usernameInput) {
                usernameInput.value = '';
            }
            if (passwordInput) {
                passwordInput.value = '';
            }
        }
        clearInputs();
        setTimeout(clearInputs, 50);
        setTimeout(clearInputs, 150);
    }
});

