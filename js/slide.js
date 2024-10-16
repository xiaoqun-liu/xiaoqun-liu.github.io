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

function previousSlide() {
    currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    showSlide(currentSlideIndex);
}

// Add keyboard navigation
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        previousSlide(); // Go to previous slide
    } else if (event.key === 'ArrowRight') {
        nextSlide(); // Go to next slide
    }
});

showSlide(currentSlideIndex);

const slideContainer = document.querySelector('.slide-container');
slideContainer.addEventListener('click', () => {
    nextSlide();
});