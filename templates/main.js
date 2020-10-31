let texts = [
  "この",
  "りんごは",
  "赤い",
  "です．",
  "あの",
  "鳥は",
  "青い",
  "です．",
  "その",
  "バナナは",
  "黄色いです．"
];

let pointer = 0;

let spanMs = 250;

let lastDate = new Date();

function render() {
  const cvs = document.getElementById('canvas'); 
  const ctx = cvs.getContext('2d');  
  const scrW = cvs.width, scrH = cvs.height;
  
  ctx.clearRect( 0, 0, scrW, scrH );
  ctx.font = "normal 30px 'Yu Gothic'";
  ctx.fillStyle = "rgb(40, 40, 40)";
  ctx.textAlign = 'center';

  ctx.fillText( texts[pointer], scrW/2, scrH/2 );

  let nowDate = new Date();

  if( nowDate-lastDate >= spanMs ) {
    pointer = (pointer + 1) % texts.length;
    lastDate = nowDate;
  }

  requestAnimationFrame( render );
}

window.onload = () => {
  sizing();

  function sizing() {
    var cvs = document.getElementById('canvas'); 
    var cntr = document.getElementById('container');

    cvs.height = cntr.offsetHeight;
    cvs.width = cntr.offsetWidth;
  }

  window.addEventListener('resize', function() {
    (!window.requestAnimationFrame) ? setTimeout(sizing, 300): window.requestAnimationFrame(sizing);
  });

  render();
}

function onSliderInput(value) {
  spanMs = value;
}