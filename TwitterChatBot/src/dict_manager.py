import os
import torch
import word_dict
import setting


# 辞書のロード。
def load_dict_saved_data(word_index_dict):
    save_data = torch.load(setting.DATABASE_DICT_SAVE_FILE_NAME)
    #save_data = torch.load(setting.DATABASE_DICT_SAVE_FILE_NAME)    # GPUのモデルをCPUに移すときはこれを使う。

    # インスタンスに直接読み込ませる。
    word_index_dict.__dict__ = save_data["word_index_dict"]

    print("辞書のロードに成功しました。")
    print()


# 保存済みの辞書をロードしてインスタンスを返す。
def dict_load():
    word_index_dict = word_dict.Dict()              # インデックス辞書の初期化
    load_dict_saved_data(word_index_dict)    # 作成済みのデータベース・辞書をロードする。
    
    return word_index_dict