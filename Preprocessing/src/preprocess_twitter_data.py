import re
import pickle
import MeCab

data_file_names = ["ですよ！tweet2020-04-13", "ですよ！tweet2020-04-14", "私tweet2020-04-09", "私はtweet2020-04-11", "私はtweet2020-04-12"]
word2vec_corpus_file_name = "jawiki.300d.word_list.pickle"

data_directory = "../before_preprocessing_data/"
save_directory = "../../seq2seq_model/corpus_data/"


def wakati(sentence):
    m = MeCab.Tagger("-Owakati")
    return m.parse(sentence)


def load_pickle(file_name):
    with open(file_name, mode='rb') as f:
        data = pickle.load(f)
        return data


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


def load_files(data_file_name):
    input_file_name = data_directory + data_file_name + "_input.txt"
    output_file_name = data_directory + data_file_name + "_output.txt"
    input = load_File(input_file_name)
    output = load_File(output_file_name)

    return input, output

def main_loop(data_file_name, wiki_corpus):
    input, output = load_files(data_file_name)  # 会話データのロード
    input, output = preprocess(input, output)   # 1対1の会話になるように前処理。

    with open(save_directory + data_file_name + "_preprocessed_input.txt", "w", encoding="utf-8") as inFile, open(save_directory + data_file_name + "_preprocessed_output.txt", "w", encoding="utf-8") as outFile:
        tmp = 0
        registered_pair_num = 0

        for i in range(len(input)):
            save_flg = True
            wakatied_input = wakati(input[i])

            for word in wakatied_input.split(" "):
                if not word in wiki_corpus:
                    print(word)
                    save_flg = False
                    tmp+=1
                    break
            
            if save_flg:
                wakatied_output = wakati(output[i])
                for word in wakatied_output.split(" "):
                    if not word in wiki_corpus:
                        print(word)
                        save_flg = False
                        tmp+=1
                        break

                if save_flg:
                    inFile.write(wakatied_input + "\n")
                    outFile.write(wakatied_output + "\n")
                    registered_pair_num += 1

        print("wikiに無い単語を含んでおり、削除されたペア数:" + str(tmp))
        print("登録ペア数:" + str(registered_pair_num))


if __name__ == "__main__":
    wiki_corpus = load_pickle(word2vec_corpus_file_name)

    for data_file_name in data_file_names:
        main_loop(data_file_name, wiki_corpus)