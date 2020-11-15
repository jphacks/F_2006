browser.contextMenus.create({
  id : "self",
  title : "選択したテキストを読む...",
  contexts : [
    "selection"
  ],
  onclick : function(info){

    // 文字を抽出 / その他項目の初期化
    var str = info.selectionText;
    var url = "https://flash-reading.herokuapp.com?sentence=true";

    // TODO: 出力
  }
});