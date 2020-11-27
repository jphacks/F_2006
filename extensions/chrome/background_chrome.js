chrome.contextMenus.create({
  title: "選択したテキストを読む...",
  contexts: [
    "selection"
  ],
  type: "normal",
  onclick: function (info) {
    const sentence = info.selectionText;

    let url = 'http://flash-reading.herokuapp.com/read?q=' + encodeURIComponent(sentence);//'https://flash-reading.herokuapp.com/read';

    // URLが長すぎる場合
    if (url.length > 2047) {
      const result = window.confirm("文章が長いので直接リンクを読み込むことができません。\nクリップボードにコピーしたうえで続行しますか。\n（新しいタブで開くのでテキストボックスに貼り付けてください。）");
      if (result == true) {
        // クリップボードにコピー
        const textArea = document.createElement("textarea");
        document.body.appendChild(textArea);
        textArea.value = sentence;
        textArea.select();
        document.execCommand("copy");

        document.body.removeChild(textArea);
        url = "http://flash-reading.herokuapp.com/read?clipboard=true";//"http://flash-reading-dev.herokuapp.com/read?clipboard=true";
      }
      else
        return;

    }
    window.open(url, 'newtab');
  }
})