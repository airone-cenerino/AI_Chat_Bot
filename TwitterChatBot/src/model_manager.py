import os
import torch
import torch.nn as nn
import network_model
import setting

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# チェックポイントでセーブされた学習済みモデルのデータをロードする。
def load_checkpoint():
    #checkpoint = torch.load(setting.MODEL_SAVE_FILE_NAME)
    checkpoint = torch.load(setting.MODEL_SAVE_FILE_NAME, map_location=torch.device('cpu'))    # GPUのモデルをCPUに移すときはこれを使う。

    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    embedding_sd = checkpoint['embedding']        
    
    return encoder_sd, decoder_sd, encoder_optimizer_sd, decoder_optimizer_sd, embedding_sd, checkpoint


# 学習済みのモデルを返す。
def get_models(dict):
    encoder_sd, decoder_sd, encoder_optimizer_sd, decoder_optimizer_sd, embedding_sd, checkpoint = load_checkpoint()  # モデルデータのロード。

    # モデル初期化
    embedding = nn.Embedding(dict.words_num, setting.hidden_size)
    encoder = network_model.EncoderRNN(setting.hidden_size, embedding, setting.encoder_n_layers, setting.dropout)
    decoder = network_model.LuongAttnDecoderRNN(setting.attn_model, embedding, setting.hidden_size, dict.words_num, setting.encoder_n_layers, setting.dropout)

    # ロード。
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)    
    print("モデルをロードしました。")
    print()

    return encoder, decoder