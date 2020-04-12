import os
import torch
import word_dict
import corpus_database
import data_loader
import setting

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



# データベースと辞書のセーブ。
def save_database_dict_saved_data(database, word_index_dict):
    directory = setting.DATABASE_DICT_SAVE_DIR

    if not os.path.exists(directory):
        os.makedirs(directory)

    torch.save({
        "corpus_database": database.__dict__,
        "word_index_dict": word_index_dict.__dict__
    }, os.path.join(directory, setting.DATABASE_DICT_SAVE_FILE_NAME))


# データベース・辞書の作成。
def make_database_dict():
    print("データベース・辞書を1から作り直します。")

    database = corpus_database.CorpusDatabase()     # コーパスのデータベース初期化
    word_index_dict = word_dict.Dict()              # インデックス辞書の初期化

    data_pairs = data_loader.corpus_data_load()          # 会話ペアリストを取得。(分かち済み)
    database.add_pairs(data_pairs, word_index_dict)      # データベース・辞書にデータを追加。
    
    database.trim_pairs(word_index_dict)  # 出現数の低い単語を含むペアは削除する。

    save_database_dict_saved_data(database, word_index_dict)  # データベース・辞書をセーブする。



# データベースと辞書のロード。
def load_database_dict_saved_data(database, word_index_dict):
    save_data = torch.load(os.path.join(setting.DATABASE_DICT_SAVE_DIR, setting.DATABASE_DICT_SAVE_FILE_NAME))
    #save_data = torch.load(os.path.join(setting.DATABASE_DICT_SAVE_DIR, setting.DATABASE_DICT_SAVE_FILE_NAME))    # GPUのモデルをCPUに移すときはこれを使う。

    # インスタンスに直接読み込ませる。
    database.__dict__ = save_data["corpus_database"]        
    word_index_dict.__dict__ = save_data["word_index_dict"]

    print("データベースと辞書のロードに成功しました。")
    print()


# 保存済みのデータベースと辞書をロードしてインスタンスを返す。
def database_dict_load():
    database = corpus_database.CorpusDatabase()     # コーパスのデータベース初期化
    word_index_dict = word_dict.Dict()              # インデックス辞書の初期化
    load_database_dict_saved_data(database, word_index_dict)    # 作成済みのデータベース・辞書をロードする。
    
    return database, word_index_dict