import asyncio
import json
import pickle

import aiomysql
import pymysql

import config

from model import *

class DBHandlerFactory():
    def __init__(self):
        self.host = config.DB_config['host']
        self.port = config.DB_config['port']
        self.user = config.DB_config['user']
        self.password = config.DB_config['password']
        self.db = config.DB_config['db']
        self.loop = asyncio.get_event_loop()

    async def create_handler(self):
        conn = await aiomysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset='utf-8', loop=self.loop, local_infile=True)
        return SqlHandler(conn)


class SqlHandler():
    def __init__(self, conn):
        self.conn = conn

    async def commit(self):
        await self.conn.commit()
        return

    async def rollback(self):
        await self.conn.rollback()
        return

    async def get_articles(self):
        pass

    async def get_metadata(self):
        pass

    async def get_articles_with_meta(self):
        c = self.conn.cursor()
        query = "SELECT `Article.aid`, `Feature.InvertedIndex`, `Article.uploadedTimestamp` from `Article` left join `Feature` on Article.aid = Feature.Aid"
        c.execute(query)
        res = c.fetchall()

        result = {}
        for r in res:
            result[r[0]] = Article.from_db_with_meta(r[0], r[1], r[2].timestamp())
        return result

    async def get_metadata(self):
        pass

    async def get_user_with_keywords(self):
        c = self.conn.cursor()
        query = "SELECT `kid` from `Interest` where `Uid` = %s"
        params = [uid]
        c.execute(query)
        res = c.fetchall()

        result = User(res)
        return result

    async def get_history(self, uid):
        c = self.conn.cursor()
        query = "SELECT `aid`, `feedback` from `ArticleHistory` where `uid` = %s"
        params = [uid]
        c.execute(query)
        res = c.fetchall()

        result = [ History(r[0], r[1]) for r in res ]
        return result

    async def push_recommendation(self):
        pass
