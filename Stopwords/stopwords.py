def get_stop_words():
    with open('Stopwords/stopwords_PT.txt', 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        f.close()
        return frozenset(stop_set)