DATABASE_DICT_SAVE_FILE_NAME = "../dict_model_data/database_dict.tar"
MODEL_SAVE_FILE_NAME = "../dict_model_data/690000_checkpoint.tar"

BOT_USER_NAME = 'cenerino_bot'
BOT_SCREEN_NAME = '@' + BOT_USER_NAME

MAX_SENTENCE_LENGTH = 25



"""学習の調整用パラメータ。設定を変えたらここも変えること！！"""
#Encoder, Decoderの設定
hidden_size = 203   # Embeddingのベクトル長
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.1

# Attentionの設定 ※そんなに変わらないらしい
#attn_model = 'dot'
attn_model = 'general'
#attn_model = 'concat'