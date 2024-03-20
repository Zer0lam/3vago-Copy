// Función para obtener datos y actualizar el gráfico
function obtenerDatosYActualizarGrafico() {
    var selectedMonth = document.querySelector('#select-month').value;

    
    fetch("/reservations_chart/" + selectedMonth)
        .then(response => response.json())
        .then(data => {
            
            console.log("Datos obtenidos:", data);

            
            updateChart(data);
        })
        .catch(error => {
            console.error("Error al obtener datos:", error);
        });
}

// Función para cargar el gráfico con datos
function updateChart(data) {
    
    var canvas = document.querySelector('#chartjs-line-chart');

    
    Chart.getChart(canvas)?.destroy();

    
    var datosAgrupados = {};

    
    data.forEach(function (item) {
        
        var fechaSinHora = item.fecha;

        
        if (!datosAgrupados[fechaSinHora]) {
            datosAgrupados[fechaSinHora] = 1; 
        } else {
            datosAgrupados[fechaSinHora]++; 
        }
    });

    
    var fechas = Object.keys(datosAgrupados);
    var reservaciones = Object.values(datosAgrupados);

    // Configurar y cargar el gráfico
    var ctx = canvas.getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechas,
            datasets: [{
                label: 'Reservations',
                data: reservaciones,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            
        }
    });
}
