import network_model
import dict_manager
import model_manager
import make_reply


def get_trained_data():
    word_index_dict = dict_manager.dict_load()  # コーパスデータベース と 単語-インデックス辞書 の取得。
    encoder, decoder = model_manager.get_models(word_index_dict)        # 学習済みモデルデータのロード。
    searcher = network_model.GreedySearchDecoder(encoder, decoder)      # 返事をするモデル。
    return encoder, decoder, searcher, word_index_dict