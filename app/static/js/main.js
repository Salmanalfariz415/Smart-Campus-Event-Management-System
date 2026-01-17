const text = document.querySelector('.colourtext');
const split = new SplitType('.colourtext', { types: 'chars' });

let ready = false;
requestAnimationFrame(() => {
  ready = true;
});

text.addEventListener("mouseenter", () => {
  if (!ready) return;

  anime({
    targets: split.chars,
    translateY: [
      { value: '-6rem', easing: 'easeOutExpo', duration: 300 },
      { value: 0, easing: 'easeOutBounce', duration: 300 }
    ],
    rotate: [0, '-1turn'],
    duration: 500,
    easing: 'easeInOutSine',
    delay: anime.stagger(50),
    loop: false
  });
});
