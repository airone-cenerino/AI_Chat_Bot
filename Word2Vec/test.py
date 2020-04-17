from gensim.models import KeyedVectors

wiki_model =  KeyedVectors.load_word2vec_format("jawiki.all_vectors.300d_sharp_trimmed.txt")
print("test")
print()
print()

similar_words_list = wiki_model.most_similar("平成", topn=10)

print("「平成」の類義語は")
for word in similar_words_list:
    print(word)
print("です。")