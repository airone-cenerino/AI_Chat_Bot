import re
import MeCab

data_directory = "../before_preprocessing_data/"
save_directory = "../../seq2seq_model/corpus_data/after_preprocessing_data/"

data_file_name = "meidai"


def wakati(sentence):
    m = MeCab.Tagger("-Owakati")
    return m.parse(sentence)

def load_File(file_name):
    file_data = []

    with open(file_name, "r", encoding="utf-8") as file:
        for sentence in file:
            file_data.append(sentence.rstrip())   # rstripは改行コードを削除するため。
    
    return file_data


# 入力と出力の文を前処理する。
def preprocess_sentence(input_sentence, output_sentence):
    # (文字列)の除去
    if "（" in input_sentence:
        input_sentence = re.sub("（[^）]+）", "", input_sentence)
    if "（" in output_sentence:
        output_sentence = re.sub("（[^）]+）", "", output_sentence)


    # ＜笑い＞の除去
    if "＜" in input_sentence:
        input_sentence = re.sub("＜[^＞]+＞", "", input_sentence)
    if "＜" in output_sentence:
        output_sentence = re.sub("＜[^＞]+＞", "", output_sentence)

    # 【大学名】の除去
    if "【" in input_sentence:
        input_sentence = re.sub("【[^】]+】", "", input_sentence)
    if "【" in output_sentence:
        output_sentence = re.sub("【[^】]+】", "", output_sentence)

    return input_sentence, output_sentence


def preprocess(input, output):
    preprocessed_input = []
    preprocessed_output = []
    
    for i in range(len(input)):
        if "＊" in input[i] or "＊" in output[i]: continue

        preprocessed_input_sentence, preprocessed_output_sentence = preprocess_sentence(input[i], output[i])
        preprocessed_input.append(preprocessed_input_sentence)
        preprocessed_output.append(preprocessed_output_sentence)


    return preprocessed_input, preprocessed_output

import chardet
if __name__ == "__main__":
    input_file_name = data_directory + data_file_name + "_input.txt"
    output_file_name = data_directory + data_file_name + "_output.txt"

    input = load_File(input_file_name)
    output = load_File(output_file_name)

    input, output = preprocess(input, output)

    with open(save_directory + data_file_name + "_preprocessed_input.txt", "w", encoding="utf-8") as inFile, open(save_directory + data_file_name + "_preprocessed_output.txt", "w", encoding="utf-8") as outFile:
        for sentence in input:
            inFile.write(wakati(sentence))
        for sentence in output:
            outFile.write(wakati(sentence))