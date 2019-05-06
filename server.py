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


class RecommendHandler(tornado.web.RequestHandler):
    async def get(self, user_id):


        article_ids = recommender.
        response = {
            'uid': user_id,
            'articles': article_ids
        }

        self.set_status(HTTPStatus.OK)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))
        self.finish()


def build_app():
    app = tornado.web.Application(
        [
            (r"/suggest/([a-z0-9]+)", RecommendHandler),
        ]
    )

    return app

if __name__  == "__main__":
    global dbf = DBHandlerFactory()
    app = build_app()
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()
