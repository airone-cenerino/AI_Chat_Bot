import torch
import word_dict

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 単語のリスト(文)をインデックスのリストに変換する。
def indexes_from_sentence(dict, sentence):
    return [dict.word2index[word] for word in sentence] + [word_dict.EOS_token]