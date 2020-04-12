import word_dict
import setting

# コーパスのデータベース。　会話のペアを蓄える。
class CorpusDatabase:
    def __init__(self):
        self.pairs = []
        self.pair_num = 0
    
    def add_pairs(self, pairs, dict):
        dict.add_pairs(pairs)       # インデックス辞書にデータを登録。

        # データベースに登録。
        for pair in pairs:
            self.pairs.append(pair)
            self.pair_num += 1


    # 出現数の低い単語を含むペアを削除する。
    def trim_pairs(self, dict):
        dict.trim()     # 出現数の少ない単語を辞書から削除

        keep_pairs = []
        for pair in self.pairs:
            input_sentence = pair[0]
            output_sentence = pair[1]
            keep_input = True
            keep_output = True

            # 文に含まれる全ての単語が辞書にあるかを確認。
            for word in input_sentence:
                if word not in dict.word2index:
                    keep_input = False
                    break
            for word in output_sentence:
                if word not in dict.word2index:
                    keep_output = False
                    break

            if keep_input and keep_output:
                keep_pairs.append(pair)

        print("辞書に登録されていない単語が使われている" + str(len(self.pairs) - len(keep_pairs)) + "個のペアを削除します。")
        print("残るペア数は" + str(len(keep_pairs)) + "個です。")
        print()

        self.pair_num = len(keep_pairs)
        self.pairs = keep_pairs