import os
import math
import gc
import time
import operator

from collections import Counter

from config import recommender_config
from model import *


class Recommender():
    def __init__(self, articles):
        self.articles = articles

    def update(self, articles):
        self.articles = articles

    def recommend(self, user):
        rank = []
        for aid in list(self.articles.keys()):
            if aid in user.skips:
                continue
            interest = 0
            for k in self.articles[aid].keywords:
                if k in user.interests:
                    interest += user.interests[k]
            passed = time.time()-self.articles[aid].timestamp
            divider = max(math.log(passed/recommender_config['time_divider'])+1,1)
            rank.append((aid, interest/divider))
        rank = sorted(rank, reverse=True, key=operator.itemgetter(1))
        return rank[:10]
