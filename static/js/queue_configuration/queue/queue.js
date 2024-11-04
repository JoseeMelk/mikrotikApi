const tablaDispositivos = document.getElementById('tablaDispositivos');
const dispositivoInput = document.getElementById('dispositivo');
const subidaInput = document.getElementById('subida');
const bajadaInput = document.getElementById('bajada');

tablaDispositivos.addEventListener('click', (event) => {
    const fila = event.target.closest('tr');
    if (fila) {
        const filas = tablaDispositivos.getElementsByTagName('tr');
        for (let i = 0; i < filas.length; i++) {
            filas[i].classList.remove('selected');
        }
        fila.classList.add('selected');
        const celdas = fila.getElementsByTagName('td');
        dispositivoInput.value = celdas[0].innerText;
        subidaInput.value = celdas[1].innerText;
        bajadaInput.value = celdas[2].innerText;
    }
});