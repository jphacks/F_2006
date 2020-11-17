browser.contextMenus.create({
  id: "self",
  title: "選択したテキストを読む...",
  contexts: [
    "selection"
  ]
});

browser.contextMenus.onClicked.addListener(function (info, tab) {
  const sentence = info.selectionText;

  const url = 'http://localhost:5000/read?q=' + encodeURI(sentence);//'https://flash-reading.herokuapp.com/read';

  browser.tabs.create({ url });
});