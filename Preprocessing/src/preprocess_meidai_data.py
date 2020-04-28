import re
import pickle
import MeCab

DATA_DIRECTORY = "../before_preprocessing_data/"
SAVE_DIRECTORY = "../../seq2seq_model/corpus_data/"

DATA_FILE_NAME = "meidai"
WORD2VEC_CORPUS_FILE_NAME = "jawiki.200d.word_list.pickle"


def wakati(sentence):
    m = MeCab.Tagger("-Owakati")
    return m.parse(sentence).rstrip()


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

    
    # 全角英数字を半角英数字に置き換え。
    mydict = {chr(0xFF10 + i): chr(0x30 + i) for i in range(10)}    # 数字
    mydict.update({chr(0xFF21 + i): chr(0x41 + i) for i in range(26)})  # 英大文字
    mydict.update({chr(0xFF41 + i): chr(0x61 + i) for i in range(26)})  # 英小文字

    input_sentence = input_sentence.translate(str.maketrans(mydict))
    output_sentence = output_sentence.translate(str.maketrans(mydict))
    
    return input_sentence, output_sentence


def load_files():
    wiki_corpus = load_pickle(WORD2VEC_CORPUS_FILE_NAME)
    input_file_name = DATA_DIRECTORY + DATA_FILE_NAME + "_input.txt"
    output_file_name = DATA_DIRECTORY + DATA_FILE_NAME + "_output.txt"
    input = load_File(input_file_name)
    output = load_File(output_file_name)

    return wiki_corpus, input, output


def preprocess(input, output):
    preprocessed_input = []
    preprocessed_output = []
    
    for i in range(len(input)):
        if "＊" in input[i] or "＊" in output[i]: continue

        preprocessed_input_sentence, preprocessed_output_sentence = preprocess_sentence(input[i], output[i])
        if preprocessed_input_sentence == "" or preprocessed_output_sentence == "":
            continue

        preprocessed_input.append(preprocessed_input_sentence)
        preprocessed_output.append(preprocessed_output_sentence)
        print(preprocessed_input_sentence)
        print(preprocessed_output_sentence)
        print()


    return preprocessed_input, preprocessed_output


def save_pairs(wiki_corpus, input, output):
    with open(SAVE_DIRECTORY + DATA_FILE_NAME + "_preprocessed_input.txt", "w", encoding="utf-8") as inFile, open(SAVE_DIRECTORY + DATA_FILE_NAME + "_preprocessed_output.txt", "w", encoding="utf-8") as outFile:
        tmp = 0
        for i in range(len(input)): # 1対ずつ保存していく。
            save_flg = True
            wakatied_input = wakati(input[i])

            for word in wakatied_input.split(" "):
                if not word in wiki_corpus:
                    #print(word)
                    save_flg = False
                    tmp+=1
                    break
            
            if save_flg:
                wakatied_output = wakati(output[i])
                for word in wakatied_output.split(" "):
                    if not word in wiki_corpus:
                        #print(word)
                        save_flg = False
                        tmp+=1
                        break

                if save_flg:
                    inFile.write(wakatied_input + "\n")
                    outFile.write(wakatied_output + "\n")


if __name__ == "__main__":
    wiki_corpus, input, output = load_files()   # word2vecの単語リストと会話データのロード
    input, output = preprocess(input, output)   # 文の前処理
    #save_pairs(wiki_corpus, input, output)      # 保存