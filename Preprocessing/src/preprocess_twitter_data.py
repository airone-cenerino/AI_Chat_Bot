import re
import MeCab

data_directory = "../before_preprocessing_data/"
save_directory = "../../seq2seq_model/corpus_data/"



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
    input_sentence = input_sentence.split("。")[0] + "。"
    output_sentence = output_sentence.split("。")[0] + "。"

    return input_sentence, output_sentence


def preprocess(input, output):
    preprocessed_input = []
    preprocessed_output = []
    
    for i in range(len(input)):
        if len(input[i]) > 50: continue
        if "【" in input[i] or "【" in output[i]: continue
        if "[" in input[i] or "[" in output[i]: continue
        
        preprocessed_input_sentence, preprocessed_output_sentence = preprocess_sentence(input[i], output[i])

        if len(preprocessed_input_sentence) < 2 or len(preprocessed_output_sentence) < 2: continue
        
        preprocessed_input.append(preprocessed_input_sentence)
        preprocessed_output.append(preprocessed_output_sentence)

    return preprocessed_input, preprocessed_output


def main_loop(data_file_name):
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


if __name__ == "__main__":
    data_file_names = ["ですよ！tweet2020-04-13", "ですよ！tweet2020-04-14", "私tweet2020-04-09", "私はtweet2020-04-11", "私はtweet2020-04-12"]

    for data_file_name in data_file_names:
        main_loop(data_file_name)