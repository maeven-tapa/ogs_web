const notice = document.querySelector('#portal-notice');
document.querySelectorAll('[data-portal-notice]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    notice.showModal();
  });
});
document.querySelectorAll('[data-close-dialog]').forEach(button => {
  button.addEventListener('click', () => notice.close());
});
notice?.addEventListener('click', event => {
  const box = notice.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) notice.close();
});

// Manual navigation keeps posts still while someone reads or uses the embed.
document.querySelectorAll('[data-post-carousel]').forEach(carousel => {
  const slides = [...carousel.querySelectorAll('.updates-slide')];
  const dots = [...carousel.querySelectorAll('[data-carousel-index]')];
  const position = carousel.querySelector('[data-carousel-position]');
  let current = 0;

  function sizeAndLoadPost(slide) {
    const viewport = slide.querySelector('.facebook-viewport');
    const frame = slide.querySelector('iframe');
    const available = Math.floor(viewport.getBoundingClientRect().width);
    if (!available) return;
    const width = Math.max(350, Math.min(500, available));
    const scale = Math.min(1, available / width);
    const height = Math.ceil(viewport.clientHeight / scale);
    frame.style.width = `${width}px`;
    frame.style.height = `${height}px`;
    frame.style.transform = `scale(${scale})`;
    const url = new URL(frame.dataset.embedUrl);
    url.searchParams.set('width', width);
    if (frame.getAttribute('src') !== url.href) frame.src = url.href;
  }

  function showPost(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    dots.forEach((dot, i) => {
      if (i === current) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
    position.textContent = current + 1;
    sizeAndLoadPost(slides[current]);
  }

  carousel.querySelector('[data-carousel-previous]').addEventListener('click', () => showPost(current - 1));
  carousel.querySelector('[data-carousel-next]').addEventListener('click', () => showPost(current + 1));
  dots.forEach((dot, i) => dot.addEventListener('click', () => showPost(i)));
  carousel.querySelector('.carousel-controls').addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = current + 1;
    else if (event.key === 'ArrowLeft') next = current - 1;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = slides.length - 1;
    else return;
    event.preventDefault();
    showPost(next);
    dots[current].focus();
  });
  carousel.querySelector('.carousel-controls').hidden = false;
  sizeAndLoadPost(slides[current]);
  if ('ResizeObserver' in window) {
    new ResizeObserver(() => sizeAndLoadPost(slides[current])).observe(carousel);
  } else {
    window.addEventListener('resize', () => sizeAndLoadPost(slides[current]));
  }
});
