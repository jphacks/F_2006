* DB 設定をしていない場合は以下を行ってください
  * Docker をインストールしてください
  * F_2006 ディレクトリ直下で `docker-compose up -d`
  * `docker-compose exec db /bin/bash` でコンテナ内へ入る
  * `psql flash-reading-db -U admin`
  * F_2006/db/db.ddl をコピペして SQL 実行
  * `exit` で終了

* 起動
  * F_2006 直下で `python ./main.py`
  * エラーが出たら `pip` で必要なパッケージをインストール
  * 特に `sqlalchemy` の他に `psycopg2` もインストールしてください (Windows10 の場合エラーが出るかも: https://stackoverflow.com/questions/36846579/error-when-installing-psycopg2-on-windows-10)
  * `localhost:5000` にアクセス