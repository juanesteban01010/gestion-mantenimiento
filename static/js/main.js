// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

document.addEventListener("click", function (event) {
  // Verifica si el clic está fuera del menú y del botón de toggle
  if (!navigation.contains(event.target) && !toggle.contains(event.target)) {
    navigation.classList.remove("active");
    main.classList.remove("active");
  }
})

// Permitir arrastrar y soltar en las columnas
function allowDrop(event) {
  event.preventDefault();
}

function drag(event) {
  event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
  event.preventDefault();
  var data = event.dataTransfer.getData("text");
  var card = document.getElementById(data);
  var columnId = event.target.id;

  if (event.target.classList.contains('kanban-column')) {
      if (columnId === "ot_en_proceso") {
          document.getElementById("solicitudNumero").value = card.id.split('-')[1];
          document.getElementById("tecnicoModal").style.display = "block"; // Mostrar modal para asignar técnico
      } else {
          event.target.appendChild(card);
          updateSolicitudState(card, columnId); // Actualizar estado si se mueve a otra columna
      }
  }
}

// Cerrar el modal
function closeModal() {
  document.getElementById("tecnicoModal").style.display = "none";
}

// Enviar el formulario del modal al servidor
document.getElementById("tecnicoForm").addEventListener("submit", function(event) {
  event.preventDefault();

  var nombreTecnico = document.getElementById("tecnico_asignado").value;
  var fechaActividad = document.getElementById("fecha_actividad").value;
  var numeroSolicitud = document.getElementById("solicitudNumero").value;

  // Enviar los datos al servidor mediante fetch
  fetch('/solicitudes/gestion_ot/', {  // Cambia '/actualizar_solicitud/' por tu URL correcta
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}'  // Asegúrate de que se maneje el CSRF token
      },
      body: JSON.stringify({
          numero: numeroSolicitud,
          estado: "OT en Proceso",
          tecnico: nombreTecnico,
          fecha: fechaActividad
      })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Error en la actualización');
      }
      return response.json();
  })
  .then(data => {
      console.log('Actualización exitosa:', data);
      
      // Mueve la tarjeta a la columna "OT en Proceso"
      var targetColumn = document.getElementById("ot_en_proceso");
      var card = document.getElementById("card-" + numeroSolicitud);
      targetColumn.appendChild(card);

      // Cierra el modal
      closeModal();
  })
  .catch((error) => {
      document.getElementById("modalError").style.display = "block";  // Mostrar error en el modal
      console.error('Error:', error);
  });
});


// modal.js o tu archivo JavaScript existente

function openModal(solicitud) {
  document.getElementById("numero_activo").value = solicitud.numero;
  document.getElementById("fecha_actividad").value = "";  // Establece el valor deseado
  document.getElementById("tecnico_asignado").value = "";  // Establece el valor deseado
  document.getElementById("estado").value = "OT en Proceso";  // Valor predeterminado
  document.getElementById("tecnicoModal").style.display = "block";
}

// Cierra el modal
function closeModal() {
  document.getElementById("tecnicoModal").style.display = "none";
}
