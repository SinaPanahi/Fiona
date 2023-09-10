// Home Page Carousel
const slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function showSlide(index) {
  slides.forEach((slide) => {
    slide.classList.remove('active');
  });
  slides[index].classList.add('active');
}

function nextSlide() {
  currentSlide++;
  if (currentSlide >= slides.length) {
    currentSlide = 0;
  }
  showSlide(currentSlide);
}

if(slides.length){
  showSlide(currentSlide);
  setInterval(nextSlide, 4000);
}


// Add to Cart
function addToCart(){
  let buttons = document.querySelectorAll('.add-to-cart');
  if (buttons.length) {
    buttons.forEach(async button => {
      button.addEventListener('click', async (e)=>{
        e.preventDefault();
        let currentLocation = window.location.href;
        let targetLocation = currentLocation.substring(0, currentLocation.indexOf('gallery')) + 'add-to-cart';
        let response = await fetch(targetLocation, {
          method: 'POST', 
          body: JSON.stringify({painting_id : button.dataset.paintingId}),
          headers: {
            "Content-Type": "application/json"
          }
        });
        const jsonData = await response.json();
        console.log(jsonData);
      })
    });
  }
}

// Remove From Cart
function RemoveFromCart(){
  let buttons = document.querySelectorAll('.remove-from-cart');
  if (buttons.length) {
    buttons.forEach(async button => {
      button.addEventListener('click', async (e)=>{
        e.preventDefault();
        let currentLocation = window.location.href;
        let targetLocation = currentLocation.substring(0, currentLocation.indexOf('gallery')) + 'remove-from-cart';
        let response = await fetch(targetLocation, {
          method: 'POST', 
          body: JSON.stringify({painting_id : button.dataset.paintingId}),
          headers: {
            "Content-Type": "application/json"
          }
        });
        const jsonData = await response.json();
        paintingId = jsonData[2];
        let removedPainting = document.querySelector(`[data-painting-id="${paintingId}"]`).parentElement;
        removedPainting.remove();
        console.log(jsonData);
      })
    });
  }
}

function showFlashMessages(){
  messageElement = document.querySelector('#flash-messages')
  rightPercentage = 100;
  if(messageElement){
    let interval = setInterval(()=>{
      messageElement.style.right = `calc(0px - ${rightPercentage}%)`;
      rightPercentage--;
      if (rightPercentage <=0){
        clearInterval(interval)
      }
    },10);
  }
}

addToCart();
RemoveFromCart();
// showFlashMessages();