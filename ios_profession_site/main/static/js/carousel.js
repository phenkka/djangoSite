document.addEventListener('DOMContentLoaded', () => {
  const carousels = document.querySelectorAll('.carousel-container');

  carousels.forEach((carousel) => {
    const wrapper = carousel.querySelector('.carousel-wrapper');
    const slides = wrapper.children;
    const slidesCount = slides.length;
    let currentIndex = 0;

    const btnPrev = carousel.querySelector('.arrow-left');
    const btnNext = carousel.querySelector('.arrow-right');

    function updateCarousel() {
      wrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    btnPrev.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + slidesCount) % slidesCount;
      updateCarousel();
    });

    btnNext.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % slidesCount;
      updateCarousel();
    });

    // Обнуляем scroll и задаём нужный CSS переход
    wrapper.style.transition = 'transform 0.5s ease';
    updateCarousel();
  });
});
