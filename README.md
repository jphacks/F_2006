# Flash Reading
## 製品ページ（画像クリックでジャンプします）
[![unknown](https://user-images.githubusercontent.com/61216147/97867819-e6ff9c80-1d51-11eb-8c5d-4e82e9e47f44.png)](https://flash-reading.herokuapp.com/)

## 製品概要
### 紹介動画（画像クリックでジャンプします）
[![IMAGE ALT](http://img.youtube.com/vi/XPKoUpRGA2c/0.jpg)](http://www.youtube.com/watch?v=XPKoUpRGA2c "紹介動画")

### 制作動機
#### 「オンライン授業、今日は解説がGoogle Documentで配布されてる。」<br>

　昨今あらゆる面でデジタル化が進み、一般的なドキュメントは勿論、スライドや画像、音声、動画などの様々な形の資料が多く出回るようになりました。<br>
　特に新型コロナウイルス(COVID-19)の流行後、「集会、近距離での会話、閉鎖空間」の所謂三密を避ける為にオンサイトな交流を減らす必要が出てきました。
その為、今までオンサイトで使用していたスライドや、配布していた紙媒体の資料、口頭で伝えていたような内容を組織間で共有するための**プライベートなデジタル文書**がオンライン上で共有されるようになりました。

#### 「長すぎでしょ。」

　しかし、そんな共有されるデジタル文書の中には、まとまりの悪い文書であったり、画像なしの文章だけが延々と描かれている文書があります。<br>
　いかに大事な書類であっても、読み手にとって気分の良いものではありませんし、概要把握だけで時間が要する、長時間の集中で重要な箇所を見落とすなどの危険性があります。<br>

　このことを解決するために私たちはFlash Readingを製作しました。<br><br>

### 製品概要
* この製品は、高速逐次視覚提示を用いて、テキストボックスにコピー&ペーストされたテキストを区切って表示します。
* 任意のテキストをコピー&ペーストして再生ボタンを押すことで、文節ごとに区切られたテキストを次々に表示していきます。
* ユーザーとしてログインすることで、一度読み取ったテキストデータを保存することができます。

### 特長
#### 特長1: 「みんなの『素早く』『読みたい』にあわせて」
* 任意のテキストをテキストボックスにコピー&ペーストしたら自動的に文節で区切るため、読みたい文書を高速に読むことができます！
* Flash Reading制作メンバー厳選の六種類のテーマカラーから好きなテーマを選択可能！お好きなテーマカラーで読むことができます！
* 読むことが疲れたらやめましょう。ログインすれば文書を保存して次回から続きをそのまま閲覧することができます！

#### 特長2: 「コピペすらも面倒だよね？」
* 任意のPDFテキストや画像をドラッグアンドドロップすることで、ファイル内のテキストを抽出！そのまま内容を閲覧することができます！

#### 特長3: 「『たまには落ち着いて読みたい』も叶えます！」
* 表示速度を変更することが可能！**自分の読みたい速度**で読むことができます！落ち着いて読むときも目線を動かす必要はもうありません！

### 解決出来ること
　わたしたちは中央に流れてくる文字を見ているだけでいいので、この製品があればもう文章を読むために目線を移動させる必要はありません！また、膨大な文章を目の当たりにしたとしても、それを少しずつ読むことができるので文章だけが延々と続く威圧的な文書も気軽に読み始めることができます！

### 今後の展望
* 今回、形態素解析を用いて解析したのは日本語だけで、英語は単純な単語での分割だけを行った。もし改善するのであれば、英語も形態素解析をかけてより正確な分割を行いたい。


### 注力したこと（こだわり等）
* 全文表示の所について、透明度の計算や行が移る動きを結構工夫した。
* OCRで読み取った文章を使いやすいように整形した。
* DBやログイン機能から、Docker, CircleCIまで、普段の業務で見聞きしてきた技術を積極的に導入した。
* 実際に表示される文字が長くなると一瞬で消えてくためにかえって読みにくくなると思い、形態素解析によって単語分割されてモノを、単に文節分割にするだけでなく、文字数によっても分割するような仕組みにした。

## 開発技術
### 活用した技術
#### PaaS
* Heroku

#### フロントエンド
* HTML5
* Javascript
* Bootstrap
* PDF.js
* Tesseract.js

#### バッグエンド
* Python
* Flask
* Postgres
* gooラボAPI
* marshmallow
* SQLAlchemy

#### 開発環境
* CircleCI
* docker
* Visual Studio Code
  
<br/><br/>
  
![heroku-1](https://user-images.githubusercontent.com/61216147/98361141-56d19800-206e-11eb-8f25-d07c4b8e5a44.png)　![HTML5_sticker](https://user-images.githubusercontent.com/61216147/98361309-a31cd800-206e-11eb-9434-e019c24410fb.png)　![bootstrap-5](https://user-images.githubusercontent.com/61216147/98361380-c6e01e00-206e-11eb-8348-48618d8ecc22.png)　![logo (2)](https://user-images.githubusercontent.com/61216147/98361500-fc850700-206e-11eb-9097-e02718f889d1.png)　![tesseract](https://user-images.githubusercontent.com/61216147/98361582-25a59780-206f-11eb-9a1b-d736e882439a.png)　![python-logo-master-v3-TM-flattened](https://user-images.githubusercontent.com/61216147/98361666-4bcb3780-206f-11eb-8fb3-2674d02af3a9.png)　![flask](https://user-images.githubusercontent.com/61216147/98361764-7fa65d00-206f-11eb-89bd-811705a32333.png)　![view@2x](https://user-images.githubusercontent.com/61216147/98361867-a6649380-206f-11eb-9f1b-7210ba80b12a.png)　![horizontal-logo-monochromatic-white](https://user-images.githubusercontent.com/61216147/98361929-c005db00-206f-11eb-8eef-c70417548671.png)　![1000px-Visual_Studio_Code_1 35_icon svg](https://user-images.githubusercontent.com/61216147/98362067-f5aac400-206f-11eb-967a-2093bb122068.png)
