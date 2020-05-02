import database_dict_manager

file_dir = "../word2vec_corpus/"

if __name__ == "__main__":
    database, word_index_dict = database_dict_manager.database_dict_load()  # コーパスデータベース と 単語-インデックス辞書 の取得。
    print(word_index_dict.word2index)

    with open(file_dir + "dict_word_list.txt", "w", encoding="utf-8") as outFile:
        for word, index in word_index_dict.word2index.items():
            outFile.write(word + "\n")