var carousel = document.querySelector('.carousel');
var cellCount = 9;
var selectedIndex = 0;

var urlParams = new URLSearchParams(window.location.search);
var n = urlParams.get('n_pics');

//var n = 12
for (var i = 0; i < n; i++) {
  var div = document.createElement("div");
  div.className = 'carousel__cell';
  var ith = Math.round(i*360/n);
  div.innerHTML = i+1;
  div.style.background = 'hsla('+ ith +', 100%, 50%, 0.8)'
  div.style.transform = 'rotateY('+ith+'deg) translateZ(500px)'
  carousel.appendChild(div);
}

function rotateCarousel() {
  var angle = selectedIndex / cellCount * -360;
  carousel.style.transform = 'translateZ(-500px) rotateY(' + angle + 'deg)';
}

var prevButton = document.querySelector('.previous-button');
prevButton.addEventListener( 'click', function() {
  selectedIndex--;
  rotateCarousel();
});

var nextButton = document.querySelector('.next-button');
nextButton.addEventListener( 'click', function() {
  selectedIndex++;
  rotateCarousel();
});

function rotate_periodically() {
  selectedIndex++;
  rotateCarousel();
}
var interval = setInterval(rotate_periodically, 3000)