chrome.contextMenus.create({
  title: "選択したテキストを読む...",
  contexts: [
    "selection"
  ],
  type: "normal",
  onclick: function (info) {
    const sentence = info.selectionText;

    const url = 'http://localhost:5000/read?q=' + encodeURI(sentence);//'https://flash-reading.herokuapp.com/read';

    window.open(url, 'newtab');
  }
})