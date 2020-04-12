import torch
import process_data
import setting
import MeCab

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 文を句構造解析して単語のリストを返す。
def wakati(sentence):
    m = MeCab.Tagger("-Owakati")
    return m.parse(sentence).rstrip().split(" ")


def evaluate(encoder, decoder, searcher, voc, sentence, max_length=setting.MAX_SENTENCE_LENGTH):
    ### Format input sentence as a batch
    # words -> indexes
    indexes_batch = [process_data.indexes_from_sentence(voc, sentence)]

    # Create lengths tensor
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # Transpose dimensions of batch to match models' expectations
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)


    # Use appropriate device
    #input_batch = input_batch.to(device)
    #lengths = lengths.to(device)

    # Decode sentence with searcher
    tokens, scores = searcher(input_batch, lengths, max_length)

    # indexes -> words
    decoded_words = [voc.index2word[token.item()] for token in tokens]
    return decoded_words


# 入力文を受け取って返事の文を返す。
def evaluateInput(encoder, decoder, searcher, voc, input_sentence):
    try:
        input_sentence = wakati(input_sentence)
        output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]

        output = ""
        for word in output_words:
            if word == "。" or word == "！" or word =="？":
                output += word
                break
            output += word

        return output
    except KeyError:
        return "辞書に登録されていない単語が含まれています。"