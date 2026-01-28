const text = document.querySelector('.colourtext');
const split = new SplitType('.colourtext', { types: 'chars' });

window.addEventListener('load', () => {
  gsap.registerPlugin(Draggable);
  const container = document.querySelector('.event-cards');

  Draggable.create(container, {
    type: "x",
    bounds: {
      maxX: 0, // Stops the leftmost card from moving right
      minX: window.innerWidth - container.offsetWidth - 100 // Stops after the last card
    },
    inertia: true,
    edgeResistance: 0.8,
  });
});

let ready = false;
requestAnimationFrame(() => {
  ready = true;
});

text.addEventListener("mouseenter", () => {
  if (!ready) return;

  anime({
    targets: split.chars,
    translateY: [
      { value: '-3rem', easing: 'easeOutExpo', duration: 300 },
      { value: 0, easing: 'easeOutBounce', duration: 300 }
    ],
    rotate: [0, '-1turn'],
    duration: 500,
    easing: 'easeInOutSine',
    delay: anime.stagger(50),
    loop: false
  });
});

