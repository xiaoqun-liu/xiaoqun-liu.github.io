const slides = document.querySelectorAll('.slide');
let currentSlideIndex = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.style.display = i === index ? 'block' : 'none';
  });
}

function nextSlide() {
  currentSlideIndex = (currentSlideIndex + 1) % slides.length;
  showSlide(currentSlideIndex);
}

// 每 5 秒自动切换到下一张幻灯片
// setInterval(nextSlide, 5000);

showSlide(currentSlideIndex);

const slideContainer = document.querySelector('.slide-container');
slideContainer.addEventListener('click', () => {
//   clearInterval(autoSlideInterval);
  nextSlide();
});