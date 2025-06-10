const wheel = document.getElementById('wheel');
const button = document.getElementById('spinButton')
const result = document.getElementById('gameResult');

let currentRotation = 0;
let spinAgain = true;

function game() {
  if (spinAgain) {  
    const numberOfItems = 4;
    const degreePerItem = 360 / numberOfItems;
    // Randomly spins somewhere between 4-7 spins
    const numRandomSpins = Math.floor(Math.random() * 4) + 4;
    const randomExtraDeg = Math.ceil(Math.random() * 360);
    const spinnDeg = numRandomSpins * 360 + randomExtraDeg;
    currentRotation += spinnDeg;

    // Trigger the transition: transform 4s ease-out; in the css
    // Animates the rotation
    // Wait for animation to end before displaying result
    wheel.style.transform = `rotate(${currentRotation}deg)`;

    // This calculates how many degrees moved reltive to origin
    setTimeout(() => {
      const degMovedFromOrigin = currentRotation % 360; // Takes away all full rotations
      // Index is waht the pointer points at. +90 fordi offset from starting point in css withc is 0deg on left.
      // + degreePerItem / 2 Fixes bias problem toward last segment. There might be asymetry between 
      // seen point and calculated point without.
      const pointPontedAt = Math.floor(((360 - degMovedFromOrigin + 90 + degreePerItem / 2) % 360) / degreePerItem);
      const listElements = wheel.querySelectorAll('li');
      let segmentFound = listElements[pointPontedAt].textContent;
      console.log(segmentFound);
      if (segmentFound != 'Spin again') {
        spinAgain = false;
      }
      // segmentFound = 'Win';
      // segmentFound = 'No prize';
      if (segmentFound === 'Win') {
        result.textContent = `Result ${segmentFound}`;
        result.className = 'success';
        tokensHandler(10);
      }
      else if (segmentFound === 'No prize') {
        result.textContent = `Result ${segmentFound}`;
        result.className = 'error';
        tokensHandler(0)        
      }
      else {
        result.textContent = `Result ${segmentFound}`;
        result.className = 'spinAgain'
      };
      }, 4000);
}}

async function tokensHandler(tokens) {
    const response = await fetch('/game', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tokens })
    });
    if (response.ok) {
        console.log('Tokens recived in flask');
        setTimeout(() => {
          window.location.href = "/";  
        }, 2000);
        
    } else {
        console.error('Failed flask');
    }
}

button.addEventListener('click', game)


  