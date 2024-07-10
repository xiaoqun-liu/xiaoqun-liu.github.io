const slides = document.querySelectorAll('.slide');
let currentSlideIndex = 0;

function showSlide(index) {
    //   slides.forEach((slide, i) => {
    //     slide.style.display = i === index ? 'block' : 'none';
    //   });
    slides.forEach((slide, i) => {
        if (i === index) {
            slide.style.display = 'block';
            slide.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            slide.style.display = 'none';
        }
    });
}

function nextSlide() {
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    showSlide(currentSlideIndex);
}

showSlide(currentSlideIndex);

const slideContainer = document.querySelector('.slide-container');
slideContainer.addEventListener('click', () => {
    //   clearInterval(autoSlideInterval);
    nextSlide();
});