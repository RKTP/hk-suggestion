import asyncio
import os
import sys
import json
import time

from http import HTTPStatus
from os import path

import tornado
import tornado.ioloop
import tornado.httpserver

from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado import web, escape, log

from recommender import *
from db import *

import pymysql


class RecommendHandler(tornado.web.RequestHandler):
    async def post(self, user_id):
        sys.stderr.write("Request from {} / recommend articles for {}\n".format(self.request.remote_ip, user_id))
        try:
            dbc = await dbf.create_handler()

            history = await dbc.get_history(user_id)
            user = await dbc.get_user_with_keywords(user_id)
            #if user is None:
            #    sys.stderr.write("history or user not exists\n")
            #    self.set_status(HTTPStatus.NOT_FOUND)
            #    self.finish()
            #    return
            user.build_interest(recommender.articles, history)

            article_ids = recommender.recommend(user)

            await dbc.push_recommendation(user_id, article_ids)
        except pymysql.err.MySQLError as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            sys.stderr.write(str(e))
            self.finish()
            return
        except Exception as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            sys.stderr.write(str(e))
            self.finish()
            return

        self.set_status(HTTPStatus.CREATED)
        self.finish()


class UpdateHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            await init_recommender()
        except pymysql.err.MySQLError as e:
            sys.stderr.write(str(e))
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.finish()
            return
        except Exception as e:
            sys.stderr.write(str(e))
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.finish()
            return

        self.set_status(HTTPStatus.OK)
        self.finish()


def build_app():
    app = tornado.web.Application(
        [
            (r"/suggest/([a-z0-9-]+)", RecommendHandler),
            (r"/update", UpdateHandler)
        ]
    )

    return app

async def init_recommender():
    global recommender
    dbc = await dbf.create_handler()
    try:
        articles = await dbc.get_articles_with_meta()
        recommender = Recommender(articles)
    except Exception as e:
        sys.stderr.write(str(e))
    sys.stderr.write("Model loading complete\n")

if __name__  == "__main__":
    global dbf
    dbf = DBHandlerFactory()
    l = asyncio.get_event_loop()
    l.run_until_complete(init_recommender())
    app = build_app()
    app.listen(5555)
    sys.stderr.write("Server starts\n")
    tornado.ioloop.IOLoop.current().start()
