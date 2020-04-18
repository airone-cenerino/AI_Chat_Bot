import MeCab
import setting

PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token

# 単語とインデックスの辞書に関するクラス。
class Dict:
    def __init__(self):
        self.trimmed = False
        self.word2index = {}    # 単語からインデックスへの辞書
        self.word2count = {}    # 単語の出現数
        self.index2word = {0: "P_A_D", 1: "S_O_S", 2: "E_O_S"}  # インデックスから単語への辞書
        self.words_num = 3  # Count PAD, SOS and EOS　　　登録単語数

    # ペアの文を辞書に追加する。
    def add_pairs(self, pairs):
        prev_words_num = self.words_num
        for pair in pairs:
            self.add_sentence(pair[0])
            self.add_sentence(pair[1])
        
        print("ペアに含まれる単語を辞書に登録しました。")
        print(str(self.words_num-prev_words_num) + "語を登録しました。")
        print("現在の登録単語数は" + str(self.words_num) + "です。")
        print()


    # 行を句構造解析して、単語を辞書に追加する。
    def add_sentence(self, sentence):
        for word in sentence:
            self.add_word(word)


    # 辞書に単語を追加する
    def add_word(self, word):
        if word not in self.word2index:     # 辞書に未登録のとき
            self.word2index[word] = self.words_num
            self.word2count[word] = 1
            self.index2word[self.words_num] = word
            self.words_num += 1
        else:
            self.word2count[word] += 1


    # 閾値未満の出現数の単語を辞書から削除する。
    def trim(self):
        if self.trimmed:
            return
        self.trimmed = True

        print("出現数の少ない単語を辞書から削除します。")

        keep_words = []

        for word, count in self.word2count.items():
            if count >= setting.TRIMMED_WORD_MAX_OCCURENCE_NUM:
                keep_words.append(word)

        print(str(len(self.word2index) - len(keep_words)) + "語を削除します。")
        print("現在の単語数は" + str(len(keep_words)) + "語です。")
        print()

        # 辞書作り直し
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.words_num = 3 # Count default tokens

        for word in keep_words:
            self.add_word(word)