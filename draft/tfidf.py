# -*- coding: utf-8 -*-

import sys
import csv
import re
from nltk.tokenize import RegexpTokenizer
import math
import random
import heapq
from operator import itemgetter, attrgetter
import czech_stemmer

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


class TfIdf:
    tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)

    def __init__(self):
        self.corpus = {}
        self.tf = {}
        self.idf = {}
        self.stopwords = set(open("../data/stopwords.txt").read().splitlines())
        #self.tfidf = {}

        self.posts = []
        self.posts_tfidf = []

        #self.tfidf = Manager().dict()

    def add_post(self, post):
        id = int(post[0])
        text = post[3]
        tokens = self.tokenizer.tokenize(text)

        self.tf[id] = {}

        for t in tokens:
            t = t.lower()
            # skip short words or stopwords
            if len(t) < 3 or t in self.stopwords:
                continue
            t = czech_stemmer.cz_stem(t)

            self.tf[id][t] = self.tf[id].get(t, 0.0) + 1.0
            if self.tf[id][t] == 1.0:
                self.corpus[t] = self.corpus.get(t, 0.0) + 1.0

        for t in self.tf[id]:
            self.tf[id][t] /= float(len(tokens))

    def calculate_tfidf(self):
        print "calculating TF-IDF..."

        for id in self.tf:
            self.posts.append(id)

            posts_tfidf = {}
            for t in self.tf[id]:
                idf = math.log(len(self.tf) / float(self.corpus[t])) + 1

                posts_tfidf[t] = self.tf[id][t] * idf

            self.posts_tfidf.append(posts_tfidf)

        print "calculating TF-IDF done"

    def cosine_similarity(self, item_idx):
        similarities = {}

        for other_idx, other_id in enumerate(self.posts):
            similarities[other_id] = 0
            norm_item_squared = 0
            norm_other_squared = 0

            for t, tfidf in self.posts_tfidf[item_idx].iteritems():
                if (self.posts_tfidf[other_idx].has_key(t)):
                    other_tfidf = self.posts_tfidf[other_idx][t]
                else:
                    other_tfidf = 0

                #other_tfidf = self.posts_tfidf[other_idx].get(t, 0.0)

                similarities[other_id] += self.posts_tfidf[item_idx][t] * other_tfidf
                norm_item_squared += self.posts_tfidf[item_idx][t] ** 2
                norm_other_squared += other_tfidf ** 2

            norm = (math.sqrt(norm_item_squared) * math.sqrt(norm_other_squared))
            if norm != 0:
                similarities[other_id] /= norm

        return similarities

cb = TfIdf()

with open('blog-posts.csv', 'rb') as postfile:
    postreader = unicode_csv_reader(postfile)
    first = True

    row_count = sum(1 for row in csv.reader(postfile))
    print "adding posts, count:", row_count, "..."
    postfile.seek(0)

    count = 0
    for row in postreader:
        if first:
            first = False
        else:
            cb.add_post(row)

        if count % 1000 == 0:
            print "progress: ", float(count) / row_count * 100, " %"
        count += 1

    print "adding posts done"


# testing - calculate tf-idf and find similarity

cb.calculate_tfidf()

for i in range(0, 100):
    item_id = cb.tf.keys()[random.randint(0, len(cb.tf) - 1)]
    similarities = cb.cosine_similarity(item_id)
    top = heapq.nlargest(5, similarities.iteritems(), key=itemgetter(1))

    print("Most similar items for item %s: %s" % (item_id, top))
