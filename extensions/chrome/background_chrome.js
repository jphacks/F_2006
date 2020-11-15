chrome.contextMenus.create({
  title : "選択したテキストを読む...",
  contexts : [
    "selection"
  ],
  type : "normal", 
  onclick : function(info){

    // 文字を抽出 / その他項目の初期化
    var str = info.selectionText;
    var url = "https://flash-reading.herokuapp.com?sentence=true";
    console.log("str = `" + str + "`");

    // TODO: 出力
  }
})