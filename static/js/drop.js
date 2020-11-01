window.addEventListener('load', () => {
  const dropDom = document.getElementById('drop-container');

  dropDom.addEventListener('dragover', (e) => {
    e.stopPropagation();
    e.preventDefault();

    dropDom.style.background = '#e1e7f0';
  }, false);

  dropDom.addEventListener('dragleave', (e) => {
    e.stopPropagation();
    e.preventDefault();

    dropDom.style.background = '#ffffff';
  }, false);

  dropDom.addEventListener('drop', (e) => {
    e.stopPropagation();
    e.preventDefault();

    dropDom.style.background = '#ffffff';

    const files = e.dataTransfer.files;

    if( files.length > 1 ) {
      return alert('一度にアップロードできるファイルは 1 つだけです');
    }

    const file = files[0];

    console.log(file);

    if( file.type === 'text/plain' ) {
      readTextFile(file);
    } else if( file.type === 'application/pdf' ) {
      readPdfFile(file);
    } else if( file.type.startsWith('image') ) {
      readImgFile(file);
    } else {
      return alert('対応していないファイル形式です');
    }
  }, false);
});

function setMainText( text ) {
  const textAreaDom = document.getElementById('main-text');
  
  textAreaDom.value = text;
}

function readTextFile( file ) {
  const fr = new FileReader();
  fr.readAsText(file);

  fr.onload = event => {
    const text = fr.result;

    setMainText(text);
  };
}

function readPdfFile( file ) {
  const fr = new FileReader();
  
  fr.onload = () => {
    const typedArray = new Uint8Array(fr.result);

    let pdf = pdfjsLib.getDocument(typedArray);
    
    return pdf.promise.then(pdf => { // get all pages text
      let maxPages = pdf.numPages;
      let countPromises = []; // collecting all page promises
      for (var j = 1; j <= maxPages; j++) {
        let page = pdf.getPage(j);

        let txt = "";
        countPromises.push(page.then(page => { // add page promise
          let textContent = page.getTextContent();

          return textContent.then(text => { // return content promise
            return text.items.map(function (s) { return s.str; }).join(''); // value page text 
          });
        }));
      }
      // Wait for all pages and join text
      return Promise.all(countPromises).then(function (texts) {
        setMainText(texts.join(''));
      });
    });
  }

  fr.readAsArrayBuffer(file);
}

function readImgFile( file ) {
  const fr = new FileReader();
  fr.readAsDataURL(file);

  fr.onload = () => {
    drawImage(fr.result);
  }
}

function drawImage( url ) {
  const cvs = document.getElementById('dummy-canvas');
  const ctx = cvs.getContext('2d');
  const image = new Image();

  image.src = url;
  image.crossOrigin = 'Anonymous';
  image.onload = () => {
    cvs.width = image.width;
    cvs.height = image.height;
    ctx.drawImage( image, 0, 0 );

    const src = ctx.getImageData( 0, 0, canvas.width, canvas.height );

    let prog = document.getElementById('tesseract-progress');

    Tesseract.recognize(src).progress(p => {
      prog.style.display = "block";
      prog.value = Math.floor(p.progress*100);
    }).then(r => {
      prog.style.display = "none";
      setMainText(r.text);
    });
  }
}