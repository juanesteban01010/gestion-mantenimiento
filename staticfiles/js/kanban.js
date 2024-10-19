document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".kanban-card");
    const columns = document.querySelectorAll(".kanban-column");

    cards.forEach(card => {
        card.draggable = true;
        card.addEventListener("dragstart", dragStart);
    });

    columns.forEach(column => {
        column.addEventListener("dragover", dragOver);
        column.addEventListener("drop", drop);
    });

    // Conexión WebSocket
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/kanban/'); // Cambia esto por tu URL de WebSocket

    socket.onmessage = function(event) {
        const nuevaSolicitud = JSON.parse(event.data);
        crearTarjeta(nuevaSolicitud);
    };

    function crearTarjeta(solicitud) {
        const columnaSolicitudes = document.querySelector('.kanban-column[data-columna="Solicitudes"]');
        const nuevaTarjeta = document.createElement('div');
        nuevaTarjeta.className = 'kanban-card';
        nuevaTarjeta.id = `card-${solicitud.id}`;
        nuevaTarjeta.innerHTML = `<h3>${solicitud.titulo}</h3><p>${solicitud.descripcion}</p>`;
        columnaSolicitudes.appendChild(nuevaTarjeta);
    }

    function dragStart(e) {
        e.dataTransfer.setData("text/plain", e.target.id);
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        const id = e.dataTransfer.getData("text");
        const card = document.getElementById(id);
        e.target.appendChild(card);
    }
});

function showKanban() {
    document.querySelector(".kanban-container").style.display = "flex";
    document.querySelector(".calendar-view").style.display = "none";
    document.querySelector(".list-view").style.display = "none";
}

function showCalendar() {
    document.querySelector(".kanban-container").style.display = "none";
    document.querySelector(".calendar-view").style.display = "block";
    document.querySelector(".list-view").style.display = "none";
}

function showList() {
    document.querySelector(".kanban-container").style.display = "none";
    document.querySelector(".calendar-view").style.display = "none";
    document.querySelector(".list-view").style.display = "block";
}

function applyDateFilter() {
    const startDate = document.getElementById("filter-date-start").value;
    const endDate = document.getElementById("filter-date-end").value;
    // Lógica para filtrar tarjetas por fecha
}
