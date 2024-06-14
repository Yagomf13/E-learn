let currentSlide = 0;
const slides = document.querySelectorAll('.carousel img');
const indicators = document.querySelectorAll('.carousel-indicators button');
let slideInterval;

function showSlide(index) {
  slides[currentSlide].classList.remove('active');
  indicators[currentSlide].classList.remove('active');
  currentSlide = index;
  slides[currentSlide].classList.add('active');
  indicators[currentSlide].classList.add('active');
  resetSlideInterval();
}

function nextSlide() {
  let nextSlide = (currentSlide + 1) % slides.length;
  showSlide(nextSlide);
}

function prevSlide() {
  let prevSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(prevSlide);
}

function resetSlideInterval() {
  clearInterval(slideInterval);
  slideInterval = setInterval(nextSlide, 3000);
}

slideInterval = setInterval(nextSlide, 3000);


// Carrusels
const boton = document.getElementById("botonBusqueda");
const carrusel = document.getElementById("carrusel");
const resultados = document.getElementById("resultados");
const busqueda = document.getElementById("busqueda");
boton.addEventListener("click", () => {
  carrusel.style.display = "none";
  resultados.style.display = "block";
})
busqueda.addEventListener("keyup", (event) => {
  console.log("Tecla presionada:", event.key);
  if (event.key === "Enter") {
    carrusel.style.display = "none";
    resultados.style.display = "block";
  }
});

//Favoritos: 

document.addEventListener('DOMContentLoaded', function() {
  const corazones = document.querySelectorAll('.corazon');
  corazones.forEach(corazon => {
      corazon.addEventListener('click', function() {
          this.textContent = this.textContent === '🖤' ? '❤️' : '🖤';
      });
  });
});