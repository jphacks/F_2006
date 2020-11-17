chrome.contextMenus.create({
  title: "選択したテキストを読む...",
  contexts: [
    "selection"
  ],
  type: "normal",
  onclick: function (info) {
    const sentence = info.selectionText;

    const url = 'http://flash-reading-dev.herokuapp.com/read?q=' + encodeURI(sentence);//'https://flash-reading.herokuapp.com/read';

    window.open(url, 'newtab');
  }
})