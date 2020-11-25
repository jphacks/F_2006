browser.contextMenus.create({
  id: "self",
  title: "選択したテキストを読む...",
  contexts: [
    "selection"
  ]
});

browser.contextMenus.onClicked.addListener(function (info, tab) {
  const sentence = info.selectionText;

  let url = 'http://flash-reading.herokuapp.com/read?q=' + encodeURI(sentence);//'https://flash-reading.herokuapp.com/read';

  // URLが長すぎる場合
  if (url.length > 2047) {
    alert('あ')

    browser.notifications.create('confirm', {
      type: "basic",
      title: "クリップボードへのコピー",
      message: "文章が長いので直接リンクを読み込むことができません。\nクリップボードにコピーしたうえで続行します。"
    });

    // クリップボードにコピー
    const textArea = document.createElement("textarea");
    document.body.appendChild(textArea);
    textArea.value = sentence;
    textArea.select();
    document.execCommand("copy");

    document.body.removeChild(textArea);
    url = "http://flash-reading.herokuapp.com/read?clipboard=true";
  }

  browser.tabs.create({ url });
});