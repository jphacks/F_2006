window.addEventListener('load', () => {
  const dropDom = document.getElementById('drop-container');

  dropDom.addEventListener('dragover', (e) => {
    e.stopPropagation();
    e.preventDefault();
  }, false);

  dropDom.addEventListener('dragleave', (e) => {
    e.stopPropagation();
    e.preventDefault();
  }, false);

  dropDom.addEventListener('drop', (e) => {
    e.stopPropagation();
    e.preventDefault();

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

let loaded = false;
let worker;

async function readImgFile( file ) {
  let prog = document.getElementById('tesseract-progress');

  prog.style.display = "block";

  if( !loaded ) {
    const { createWorker } = Tesseract;
    worker = createWorker();
    
    const loadWorker = async () => {
      await worker.load();
      await worker.loadLanguage('jpn');
      await worker.initialize('jpn');
    }

    await loadWorker()

    loaded = true;
  }

  worker.recognize(file).then(r => {
    prog.style.display = "none";
    
    const text = trimImgText(r.data.text); 
    setMainText(text);
  });
}

function trimImgText( text ) {
  const words = text.split(' ');

  const isJapanese = word => {
    for( let i = 0; i < word.length; ++i ) if( word.charCodeAt(i) >= 256 )
      return true;

    return false;
  }

  let ret = "";

  for( let i = 0; i < words.length; ++i ) {
    if( i && !isJapanese(words[i-1]) && !isJapanese(words[i]) ) {
      ret += ' ';
    }

    ret += words[i];
  }

  ret = ret.split('\n').join('');

  return ret;
}