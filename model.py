import math
import pickle as pkl

class User():
    def __init__(self, keywords):
        self.keywords = keywords
        self.interests = None
        self.skips = None

    def build_interest(self, articles, history):
        self.interests = {}
        self.skips = []

        for k in self.keywords:
            self.interests[k] = 1.5
        for h in history:
            self.skips.append(h.aid)
            if h.feedback != None:
                for k in articles[h.aid].keywords:
                    if k in self.keywords:
                        if h.feedback == None:
                            self.interests[k] = min(2.0, self.interests[k]+0.1)
                        elif h.feedback:
                            self.interests[k] = min(2.0, self.interests[k]+0.25)
                        else:
                            self.interests[k] = max(0.5, self.interests[k]-0.1)


class History():
    def __init__(self, aid, feedback=None):
        self.aid = aid
        self.feedback = feedback


class Article():
    def __init__(self, id, keywords, timestamp):
        self.id = id
        self.keywords = keywords
        self.timestamp = timestamp

    @staticmethod
    def from_db(id, keyword_blop):
        return Article(id, pkl.loads(keyword_blop))

    @staticmethod
    def from_db_with_meta(id, keyword_blop, timestamp):
        return Article(id, pkl.loads(keyword_blop), timestamp)
