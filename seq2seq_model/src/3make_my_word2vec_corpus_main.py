file_dir = "../word2vec_corpus/"
load_corpus_file_name = "jawiki.all_vectors.200d_sharp_trimmed.txt"
save_corpus_file_name = "jawiki.all_vectors.200d_mycorpus.txt"
load_wordlist_file_name = "dict_word_list.txt"


def load_File(file_name):
    file_data = []

    with open(file_name, "r", encoding="utf-8") as file:
        for sentence in file:
            file_data.append(sentence.rstrip())   # rstripは改行コードを削除するため。
    
    return file_data


if __name__ == "__main__":
    word_list = load_File(file_dir + load_wordlist_file_name)   # wordIndex辞書に格納されている単語のリスト。
    old_corpus = load_File(file_dir + load_corpus_file_name)    # Word2Vecのコーパス。

    word_vec_dict = dict()  # 新しく作るWord2Vecコーパスに加える単語とベクトルの組み合わせ。
    
    for i in range(1, len(old_corpus)):
        word_and_vec = old_corpus[i].split(" ")
        word = word_and_vec[0]
        vec = word_and_vec[1:]
        
        # word_listにあるwordだけ選別して辞書にぶち込んでみる。
        if word in word_list:
            word_vec_dict[word] = vec

    with open(file_dir + save_corpus_file_name, "w", encoding="utf-8") as outFile:
        outFile.write(str(len(word_list) + 3) + " 203\n")

        default_word = ["P_A_D", "S_O_S", "E_O_S"]
        default_word_vector =[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        for i in range(len(default_word)):
            temp = [0 for j in range(200)]
            temp.extend(default_word_vector[i])
            outFile.write(default_word[i] + " " + ' '.join(map(str, temp)) + "\n")

        for word in word_list:
            temp = word_vec_dict[word]
            temp.extend([0,0,0])
            outFile.write(word + " " + ' '.join(map(str, temp)) + "\n")