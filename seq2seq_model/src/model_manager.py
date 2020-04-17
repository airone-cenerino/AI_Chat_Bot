import os
import torch
import torch.nn as nn
import gensim
import network_model
import training
import setting

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# チェックポイントでセーブされた学習済みモデルのデータをロードする。
def load_checkpoint():
    checkpoint = torch.load(setting.load_file_name)
    #checkpoint = torch.load(setting.load_file_name, map_location=torch.device('cpu'))    # GPUのモデルをCPUに移すときはこれを使う。

    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    
    return encoder_sd, decoder_sd, encoder_optimizer_sd, decoder_optimizer_sd, checkpoint


# 学習済みのモデルを返す。
def get_models(dict):
    encoder_sd, decoder_sd, encoder_optimizer_sd, decoder_optimizer_sd, checkpoint = load_checkpoint()  # モデルデータのロード。
    wiki_corpus = gensim.models.KeyedVectors.load_word2vec_format(setting.WORD2DICT_CORPUS_FILE_DIR + setting.WORD2DICT_CORPUS_FILE_NAME)   # word2vecコーパスの読み込み
    weights = wiki_corpus.wv.syn0

    # 各モデルの初期化
    embedding = nn.Embedding(dict.words_num, setting.hidden_size)
    embedding.weight = nn.Parameter(torch.from_numpy(weights))
    encoder = network_model.EncoderRNN(setting.hidden_size, embedding, setting.encoder_n_layers, setting.dropout)
    decoder = network_model.LuongAttnDecoderRNN(setting.attn_model, embedding, setting.hidden_size, dict.words_num, setting.encoder_n_layers, setting.dropout)

    # ロード。
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)    
    print("チェックポイント" + str(setting.LOAD_MODEL_EPOCH_NUM) + "のモデルをロードしました。")
    print()

    return encoder, decoder


# モデルのセットアップをする。
def set_up_models(dict):
    print('モデルのセットアップを開始します。')

    wiki_corpus = gensim.models.KeyedVectors.load_word2vec_format(setting.WORD2DICT_CORPUS_FILE_DIR + setting.WORD2DICT_CORPUS_FILE_NAME)   # word2vecコーパスの読み込み
    weights = wiki_corpus.wv.syn0


    # 各モデルの初期化
    embedding = nn.Embedding(dict.words_num, setting.hidden_size)
    embedding.weight = nn.Parameter(torch.from_numpy(weights))

    encoder = network_model.EncoderRNN(setting.hidden_size, embedding, setting.encoder_n_layers, setting.dropout)
    decoder = network_model.LuongAttnDecoderRNN(setting.attn_model, embedding, setting.hidden_size, dict.words_num, setting.encoder_n_layers, setting.dropout)

    if setting.IS_TRAIN_FROM_THE_MIDDLE:    # ロード有
        encoder_sd, decoder_sd, encoder_optimizer_sd, decoder_optimizer_sd, embedding_sd, checkpoint = load_checkpoint()  # 学習途中のモデルの読み込み。

        # 各モデルのロード
        encoder.load_state_dict(encoder_sd)
        decoder.load_state_dict(decoder_sd)
    else:
        load_file_name = None
        checkpoint = []
        decoder_optimizer_sd=[] 
        encoder_optimizer_sd=[]

    # GPU対応
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    print('モデルのセットアップが完了しました。')
    print()

    return embedding, encoder, decoder, encoder_optimizer_sd, decoder_optimizer_sd, checkpoint


# データベースと辞書を受け取って学習する。
def model_train(database, word_index_dict):
    models_data = set_up_models(word_index_dict)  # モデルのセットアップ
    training.execute_training_model(*models_data, word_index_dict, database.pairs)    # トレーニング開始