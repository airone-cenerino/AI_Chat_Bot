import torch
import process_data
import data_loader
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


def evaluateInput(encoder, decoder, searcher, voc):
    input_sentence = ''
    while(1):
        try:
            # Get input sentence
            input_sentence = input('> ')
            # Check if it is quit case
            if input_sentence == 'q' or input_sentence == 'quit': break
            # Normalize sentence
            input_sentence = wakati(input_sentence)
            # Evaluate sentence
            output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
            # Format and print response sentence
            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]

            #print(len(output_words))
            #print(output_words)
            print('Bot:', end="")
            for word in output_words:
                if word == "。" or word == "！" or word =="？":
                    print(word)
                    break
                print(word, end="")

            print()

        except KeyError:
            print("Bot:辞書に登録されていない単語が含まれています。")