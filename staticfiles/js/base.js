class ScrollableElement {
    constructor(selector, options = {}) {
      this.element = document.querySelector(selector);
      this.scrollSpeed = options.scrollSpeed || 50;
      this.scrollDirection = options.scrollDirection || 1;
      this.attachScrollListener();
    }
  
    attachScrollListener() {
      this.element.addEventListener('wheel', (event) => {
        const isAtRightEnd = this.element.scrollLeft + this.element.clientWidth >= this.element.scrollWidth;
        const isAtLeftEnd = this.element.scrollLeft === 0;
  
        if (isAtRightEnd && event.deltaY > 0) {
          window.scrollBy(0, this.scrollSpeed * this.scrollDirection);
        } else if (isAtLeftEnd && event.deltaY < 0) {
          window.scrollBy(0, -this.scrollSpeed * this.scrollDirection);
        } else {
          const scrollDirection = event.deltaY > 0 ? this.scrollDirection : -this.scrollDirection;
          this.element.scrollLeft += this.scrollSpeed * scrollDirection;
        }
  
        event.preventDefault();
      });
    }
  }
  
  const featureSlideshowElement = document.querySelector('table');
  if (featureSlideshowElement) {
    const featureScrollable = new ScrollableElement('table', {
      scrollSpeed: 150
    });
  }