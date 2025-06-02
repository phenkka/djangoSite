document.addEventListener('DOMContentLoaded', () => {
  const wrapper = document.getElementById('carouselWrapper');
  const slidesCount = wrapper.children.length;
  let currentIndex = 0;

  const btnPrev = document.querySelector('.arrow-left');
  const btnNext = document.querySelector('.arrow-right');

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
});