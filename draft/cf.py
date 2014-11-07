import csv
import math
import random


LAMBDA8 = 100
ITEM_BASELINE_RATING = 0.5


class CFEngine:
    def __init__(self):
        super().__init__()
        self._item_ids = set()
        self._similarity = {}
        self._user_rating = {}
        self._correlation = {}
        self._user_rated_items = {}
        self._user_ratings = {}
        self._item_ratings = {}

    def correlation(self, item_id1, item_id2):
        correlation_fraction_top = 0
        correlation_fraction_bottom = 0
        for user_id, user_rated_items in self._user_rated_items.items():
            if item_id1 in user_rated_items and item_id2 in user_rated_items:
                correlation_fraction_top += (self._user_rating[user_id][item_id1] - ITEM_BASELINE_RATING) * (
                self._user_rating[user_id][item_id2] - ITEM_BASELINE_RATING)
                correlation_fraction_bottom += math.pow(self._user_rating[user_id][item_id1], 2) * math.pow(
                    self._user_rating[user_id][item_id2], 2)

        if correlation_fraction_bottom == 0:
            correlation = 0
        else:
            correlation = correlation_fraction_top / math.sqrt(correlation_fraction_bottom)



        if not item_id1 in self._correlation:
            self._correlation[item_id1] = {}
        if not item_id2 in self._correlation:
            self._correlation[item_id2] = {}

        self._correlation[item_id1][item_id2] = self._correlation[item_id2][item_id1] = correlation

    def similarity(self, item_id1, item_id2):
        n_ij = 0
        for user_id, user_rated_items in self._user_rated_items.items():
            if item_id1 in user_rated_items and item_id2 in user_rated_items:
                n_ij += 1

        if not item_id1 in self._similarity:
            self._similarity[item_id1] = {}
        if not item_id2 in self._similarity:
            self._similarity[item_id2] = {}

        self._similarity[item_id1][item_id2] = self._similarity[item_id2][item_id1] = (n_ij - 1) / (
        n_ij - 1 + LAMBDA8) * self._correlation[item_id1][item_id2]

    def predict_rating(self, user_id, item_id1):
        rating = 0

        top = 0
        bottom = 0

        for item_id2 in self._similarity[item_id1].keys():
            if item_id2 in self._user_rated_items[user_id]:
                top += self._similarity[item_id1][item_id2] * self._user_rating[user_id][item_id2]
                bottom += self._similarity[item_id1][item_id2]

        if not bottom == 0:
            rating = top / bottom

        self._user_rating[user_id][item_id1] = rating
        return rating

    def run(self, item_likes):
        for rating in item_likes:
            item_id = rating["item_id"]
            user_id = rating["user_id"]

            if not user_id in self._user_rating.keys():
                self._user_rating[user_id] = {}
            if not user_id in self._user_rated_items.keys():
                self._user_rated_items[user_id] = set()

            self._user_rating[user_id][item_id] = 1
            self._user_rated_items[user_id].add(item_id)
            self._item_ids.add(item_id)

        num_items = len(self._item_ids)

        print("total items %d" % num_items)

        item_ids_list = list(self._item_ids)

        for item_index1 in range(0, num_items):
            if item_index1 % 100 == 0:
                print("%d / %d" % (item_index1, num_items))

            for item_index2 in range(item_index1 + 1, num_items):
                item_id1 = item_ids_list[item_index1]
                item_id2 = item_ids_list[item_index2]

                self.correlation(item_id1, item_id2)
                self.similarity(item_id1, item_id2)


with open('blog-post-likes.csv', 'r') as likes:
    like_rows = csv.reader(likes, dialect=csv.excel)

    item_likes = []
    for row in like_rows:
        item_likes.append({"item_id": int(row[0]), "user_id": int(row[1])})

    item_likes = item_likes[:500]

    engine = CFEngine()
    engine.run(item_likes)

    '''args = sys.argv
    offset = 1
    if len(args) < 2:
        offset = 0
        print("Enter user_id and item_id: ")
        args = sys.stdin.readline().split()
        if len(args) < 2:
            exit(0)

    user_id = args[0 + offset]
    item_id = args[1 + offset]
    '''

    #user_id = 33682
    #item_id = 9292

    for i in range(0, 100):
        user_id = item_likes[random.randint(0, len(item_likes) - 1)]['user_id']
        item_id = item_likes[random.randint(0, len(item_likes) - 1)]['item_id']
        print("Predicting rating for user_id %s , item_id %s : %s" % (user_id, item_id, engine.predict_rating(user_id, item_id)))





