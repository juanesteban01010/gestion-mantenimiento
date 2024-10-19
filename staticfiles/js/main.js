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
