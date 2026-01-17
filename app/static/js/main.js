const text = document.querySelector('.colourtext');
const split = new SplitType('.colourtext', { types: 'chars' });

window.addEventListener('load', () => {
  gsap.registerPlugin(Draggable);

  Draggable.create(".card", {
    type: "x",
    bounds: ".event-cards",
    inertia: false,
    onDrag: function() {
      const xChange = this.deltaX; // How much the mouse moved horizontally
      const yChange = this.deltaY; // How much the mouse moved vertically
      const draggedCard = this.target;

      // Apply that same movement to all other cards
      document.querySelectorAll(".card").forEach(card => {
        if (card !== draggedCard) {
          gsap.set(card, {
            x: `+=${xChange}`,
            y: `+=${yChange}`
          });
        }
      });
    }// Set to true only if you have the InertiaPlugin
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

