import network_model
import database_dict_manager
import model_manager
import evaluate

# モード切替-----------------------------------------
TRAINING = True     # 学習ならTrue、会話モードならFalse
#---------------------------------------------------


# 学習モード
def training_mode(database, word_index_dict):
    model_manager.model_train(database, word_index_dict)   # モデルに学習させる。

# 会話モード
def evaluate_mode(word_index_dict):
    encoder, decoder = model_manager.get_models(word_index_dict)        # 学習済みモデルデータのロード。
    searcher = network_model.GreedySearchDecoder(encoder, decoder)      # 返事をするモデル。
    evaluate.evaluateInput(encoder, decoder, searcher, word_index_dict) # 入力受付開始。


def main():
    database, word_index_dict = database_dict_manager.database_dict_load()  # コーパスデータベース と 単語-インデックス辞書 の取得。

    # モード切替
    if TRAINING:
        training_mode(database, word_index_dict)
    else:
        evaluate_mode(word_index_dict)
        

if __name__ == "__main__":
    main()