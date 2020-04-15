import MeCab


file_name = "ですよ！tweet2020-04-14"


# 文を句構造解析して単語のリストを返す。
def wakati(sentence):
    m = MeCab.Tagger("-Owakati")
    return m.parse(sentence)


def load_File(file_name):
    file_data = []

    with open(file_name, "r", encoding="utf-8") as file:
        for sentence in file:
            file_data.append(sentence.rstrip())   # rstripは改行コードを削除するため。
    
    return file_data


if __name__ == "__main__":
    input_file_name = "分かち前/" + file_name + "_input.txt"
    output_file_name = "分かち前/" + file_name + "_output.txt"

    input = load_File(input_file_name)
    output = load_File(output_file_name)

    if len(input) != len(output):
        print("長さが異なります。")
        exit()

    with open(file_name + "_分かち後_input.txt", "w", encoding="utf-8") as inFile, open(file_name + "_分かち後_output.txt", "w", encoding="utf-8") as outFile:
        for sentence in input:
            inFile.write(wakati(sentence))
        for sentence in output:
            outFile.write(wakati(sentence))