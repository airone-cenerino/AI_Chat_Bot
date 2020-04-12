import torch
import word_dict
import itertools


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IS_AVAILABLE_GPU = torch.cuda.is_available()

# 単語のリスト(文)をインデックスのリストに変換する。
def indexes_from_sentence(dict, sentence):
    return [dict.word2index[word] for word in sentence] + [word_dict.EOS_token]


# 与えられたバッチをパディングし、2重リストの行と列を入れ替える。
def zero_padding(batch, fillvalue=word_dict.PAD_token):
    return list(itertools.zip_longest(*batch, fillvalue=fillvalue))


# inputのバッチをモデル用に加工する。
def inputVar(input_batch, dict):
    indexed_input_batch = [indexes_from_sentence(dict, sentence) for sentence in input_batch]  # インデックス化
    lengths = torch.tensor([len(indexes) for indexes in indexed_input_batch], device=device)                   # 各行の単語数のリスト
    padded_input_batch = zero_padding(indexed_input_batch)  # パディングと行列の変形。

    if IS_AVAILABLE_GPU:
        padded_input_batch = torch.cuda.LongTensor(padded_input_batch)  # テンソル型に変更。
    else:
        padded_input_batch = torch.LongTensor(padded_input_batch)  # テンソル型に変更。
 
    return padded_input_batch, lengths


# バッチを受け取り、パディング文字なら0を、それ以外なら1を対応させた2重リストを返す。　例:[3, 4, 5, 0, 0] -> [1, 1, 1, 0, 0]
def binary_matrix(batch, value=word_dict.PAD_token):
    m = []
    for i, seq in enumerate(batch):
        m.append([])
        for index in seq:
            if index == word_dict.PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    return m


# outputのバッチをモデル用に加工する。
def outputVar(output_batch, dict):
    indexed_output_batch = [indexes_from_sentence(dict, sentence) for sentence in output_batch] # インデックス化
    max_target_len = max([len(indexes) for indexes in indexed_output_batch])
    padded_output_batch = zero_padding(indexed_output_batch)    # パディングと行列の入れ替え。
    mask = binary_matrix(padded_output_batch)
    if IS_AVAILABLE_GPU:
        mask = torch.cuda.BoolTensor(mask)   # bool型テンソルに型変換。
        padded_output_batch = torch.cuda.LongTensor(padded_output_batch)
    else:
        mask = torch.BoolTensor(mask)   # bool型テンソルに型変換。
        padded_output_batch = torch.LongTensor(padded_output_batch)

    return padded_output_batch, mask, max_target_len


# バッチをネットワークモデルに入力するために加工する。
def batch2TrainData(dict, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0]), reverse=True)  # inputの長さでpairs_batchをsort(降順)
    
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])

    input, input_lengths = inputVar(input_batch, dict)                  # inputバッチをモデル入力のために加工。
    output, output_mask, max_target_len = outputVar(output_batch, dict) # outputバッチをモデル入力のために加工。

    return input, input_lengths, output, output_mask, max_target_len