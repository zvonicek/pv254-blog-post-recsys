# -*- coding: utf-8 -*-

import sys
import csv
import re
from nltk.tokenize import RegexpTokenizer
import math

reload(sys)
sys.setdefaultencoding("utf-8")

# helper functions to load input in utf-8
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class tf_idf:
    tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)

    def __init__(self):
        self.corpus = {}
        self.tf = {}
        self.idf = {}
        self.tfidf = {}

    def add_post(self, post):
        id = int(post[0])
        text = post[3]
        tokens = self.tokenizer.tokenize(text)

        # TODO: do some token filtering & stemming there
        # tokens = [token.lower() for token in tokens if len(token) > 2]

        self.tf[id] = {}

        for t in tokens:
            self.tf[id][t] = self.tf[id].get(t, 0.0) + 1.0
            if self.tf[id][t] == 1.0:
                self.corpus[t] = self.corpus.get(t, 0.0) + 1.0

        for t in self.tf[id]:
            self.tf[id][t] /= float(len(tokens))

    def calculate_tfidf(self):
        for id in self.tf:
            self.idf[id] = {}
            self.tfidf[id] = {}

            for t in self.tf[id]:
                self.idf[id][t] = math.log(len(self.tf) / float(self.corpus[t])) + 1
                self.tfidf[id][t] = self.tf[id][t] * self.idf[id][t]

    def cosine_similarity(self, item_id):
        similarities = {}

        for other_id in self.tfidf:
            similarities[other_id] = 0
            norm_item_squared = 0
            norm_other_squared = 0

            for t in self.tfidf[item_id]:
                similarities[other_id] += self.tfidf[item_id][t] * self.tfidf[other_id].get(t, 0.0)
                norm_item_squared += math.pow(self.tfidf[item_id][t], 2)
                norm_other_squared += math.pow(self.tfidf[other_id].get(t, 0.0), 2)

            norm = (math.sqrt(norm_item_squared) * math.sqrt(norm_other_squared))
            if norm != 0:
                similarities[other_id] /= norm

        return similarities

cb = tf_idf()

with open('blog-posts.csv', 'rb') as postfile:
    postreader = unicode_csv_reader(postfile)
    first = True

    for row in postreader:
        if first:
            first = False
        else:
            cb.add_post(row)


# testing - calculate tf-idf and find similarity
cb.calculate_tfidf()
print cb.cosine_similarity(50081)