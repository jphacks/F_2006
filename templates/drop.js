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

    readTextFile(files[0]);
  }, false);
});

function readTextFile( file ) {
  const fr = new FileReader();
  fr.readAsText(file);

  fr.onload = event => {
    const text = fr.result;
    const textAreaDom = document.getElementById('main-text');

    textAreaDom.value = text;
  };
}