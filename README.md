# AIChatBot

## 参考にしたサイト
+ https://pytorch.org/tutorials/beginner/chatbot_tutorial.html
+ https://qiita.com/gacky01/items/89c6c626848417391438
+ https://qiita.com/gacky01/items/6af16e39e6665a9285ae

## How to Use (ツイートの収集から会話まで)
1. /TwitterCrawl/private_key.pyというファイルを作成し、以下のように辞書型でTwitterAPIの鍵を記述する。

```
oath_key_dict = {
    "consumer_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "consumer_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "access_token_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```


2. `/TwitterCrawl/twitter_crawler_main.py` を実行する。この時、ツイートの検索キーワードを第1引数で指定する。

3. `/TwitterCrawl/in_out_divide.py` の `inout_file_name` を適宜変更してから `/TwitterCrawl/in_out_divide.py` を実行する。

4. `/Preprocessing/preprocess_twitter_data.py` の `data_file_names` を適宜変更してから実行して、前処理を行う。

5. `/seq2seq_model/src/setting.py` のデータベース・辞書作成に関する項目を設定してから、`/seq2seq_model/src/database_dict_main.py` を実行して、データベースと辞書を作成する。

6. `/seq2seq_model/src/setting.py` の学習モードに関する項目を設定してから、`/seq2seq_model/src/main.py` を実行してモデルに学習させる。

7. `/seq2seq_model/src/setting.py` の会話モードに関する項目を設定してから、`/seq2seq_model/src/main.py` の `TRAINING` 変数を `False` に書き変えてから `/seq2seq_model/src/main.py` を実行し、実際に対話してみる。

---

## Preprocessing
+ preprocess_twitter_data.py : Twitterから収集したリプライ対の前処理を行う。
+ preprocess_meidai_data.py : 名大会話コーパスの前処理を行う。

---

## seq2seq_model
コーパスデータを用いてseq2seqモデルの学習を行う。
### corpus_data
コーパスデータの置き場所。

---

### database_dict_data
データベースと辞書の保存場所。(git上にはないが、データベースと辞書を作れば生成されるフォルダです。)

---

### src
  + corpus_database.py : コーパスのデータベースを管理するクラス。
  + data_loader.py :  コーパスデータを読み込んでデータベースを作成する。
  + database_dict_main.py : seq2seq_model/corpus_dataのデータを読み込んで、データベース・辞書を作成するメイン関数。
  + database_dict_manager.py : データベースと辞書のを管理する。
  + evaluate.py : 会話モードで受けっとった文章をもとに返事を作成する。
  + main.py : 学習モード・会話モードのメイン関数。
  + model_manager.py : ネットワークモデルを管理する。
  + network_model.py : ネットワークモデルの構造が記述されている。
  + process_data.py : バッチデータをモデルに入力するための形式に加工する。
  + setting.py : 設定
  + training.py : モデルの学習を管理する。
  + word_dict.py : 単語とインデックスの辞書を管理するクラス。
  
---

### trained_model_data
訓練済みモデルの保存場所。(git上にはないが、モデルを訓練すれば生成されるフォルダです。)

---

## TwitterCrawl
TwitterAPIを用いて、会話データを収集する。(使う際は自分のAPIキーを辞書型に記述したprivate_key.pyを作成してください。)
  + tweet : 収集したツイートを格納するディレクトリ。
  + check_limit.py : API呼び出しの回数制限関連。
  + get_tweet.py : ツイートを取得するメイン部分。
  + in_out_divide.py : tweetディレクトリにあるデータをinとoutに分割してファイル保存する。
  + teitter_crawler_main.py : メイン関数
  
---

## TwitterChatBot
TwitterAPIを用いて自分に飛んできたリプに返事をする。
