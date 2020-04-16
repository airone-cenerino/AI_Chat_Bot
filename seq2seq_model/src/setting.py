import os

model_name = 'chatbot_ver11.0_general_pre追加'       # モデル名


"""データベース・辞書作成"""
DATABASE_DICT_SAVE_DIR = "../database_dict_data/" + model_name
DATABASE_DICT_SAVE_FILE_NAME = "database_dict.tar"

TRIMMED_WORD_MAX_OCCURENCE_NUM = 5  # 辞書から削除しない単語の最小出現数
MAX_SENTENCE_LENGTH = 20  # 1文の最大単語数 この値より長い文は使わない。

# コーパスファイル名
corpus_data_names = ["meidai", "あるtweet2020-04-09", "あるtweet2020-04-10", "です。tweet2020-04-09", "です。tweet2020-04-10", "です。tweet2020-04-11", "です。tweet2020-04-13",
                        "ですよ！tweet2020-04-13", "ですよ！tweet2020-04-14", "私tweet2020-04-09", "私はtweet2020-04-11", "私はtweet2020-04-12"]



"""学習・会話モード共通項目------------------------------------------------------------------------------"""
save_dir = "../trained_model_data"  # 学習モデルのセーブディレクトリ。
corpus_name = "meidai_and_twitter"         # コーパス名

LOAD_MODEL_EPOCH_NUM = 80000        # 途中から学習を始める際 or 会話モードで使う 学習済みモデルのエポック数。


"""学習モード----------------------------------------------------------------------------"""
IS_TRAIN_FROM_THE_MIDDLE = True     # 以前の続きから学習を再開するかどうか。



"""学習の調整用パラメータ。"""
#Encoder, Decoderの設定
hidden_size = 1000   # Embeddingのベクトル長
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.1


# Configure training/optimization
learning_rate = 0.0001
decoder_learning_ratio = 5.0


# Attentionの設定 ※そんなに変わらないらしい
#attn_model = 'dot'
attn_model = 'general'
#attn_model = 'concat'   # メモリオーバーしがち


clip = 50.0 # gradient clipping
teacher_forcing_ratio = 1.0 # 教師強制




# epoch, batch関連
iteration_num = 120000       # エポック数
save_every = 2000           # エポック何回ごとにセーブするのか。
print_every = 100           # エポック何回ごとに結果の表示をするのか。
batch_size = 32             # バッチサイズ




load_file_name = os.path.join(save_dir, model_name, corpus_name,
                    '{}-{}_{}'.format(encoder_n_layers, decoder_n_layers, hidden_size),
                    '{}_checkpoint.tar'.format(LOAD_MODEL_EPOCH_NUM))