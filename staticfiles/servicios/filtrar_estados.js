console.log("💡 JS de filtrar_estados.js cargado en el admin");

document.addEventListener("DOMContentLoaded", function () {
    const waitForElements = () => {
        const tipoSelect = document.querySelector('#id_tipo');
        const estadoSelect = document.querySelector('#id_estado');

        if (!tipoSelect || !estadoSelect) {
            console.log("⏳ Esperando campos...");
            return setTimeout(waitForElements, 100);
        }

        console.log("✅ Campos encontrados: tipo y estado");

        const tecnicoEstados = ['recibido', 'diagnosticado', 'presupuestado', 'en_reparacion', 'listo_para_entregar', 'entregado'];
        const instalacionEstados = ['cotizado', 'pendiente_instalacion', 'instalado', 'entregado'];

        // Guardar todas las opciones originales en data
        if (!estadoSelect.dataset.originalOptions) {
            estadoSelect.dataset.originalOptions = JSON.stringify(
                Array.from(estadoSelect.options).map(opt => ({
                    value: opt.value,
                    text: opt.text
                }))
            );
        }

        function filtrarEstados() {
            const tipo = tipoSelect.value;
            let estadosPermitidos = [];

            if (tipo === 'tecnico') {
                estadosPermitidos = tecnicoEstados;
            } else if (tipo === 'instalacion') {
                estadosPermitidos = instalacionEstados;
            }

            // Restaurar opciones originales
            const originalOptions = JSON.parse(estadoSelect.dataset.originalOptions);
            estadoSelect.innerHTML = ''; // Limpiar

            originalOptions.forEach(opt => {
                if (estadosPermitidos.includes(opt.value)) {
                    const option = document.createElement('option');
                    option.value = opt.value;
                    option.text = opt.text;
                    estadoSelect.appendChild(option);
                }
            });

            if (estadoSelect.options.length > 0) {
                estadoSelect.value = estadoSelect.options[0].value;
            }
        }

        tipoSelect.addEventListener('change', filtrarEstados);
        filtrarEstados();
    };

    waitForElements();
});
