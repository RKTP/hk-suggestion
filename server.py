import asyncio
import os
import sys
import json
import time

# Only used for mock handler
import random

from http import HTTPStatus
from os import path


import tornado
import tornado.ioloop
import tornado.httpserver

from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado import web, escape, log

import pymysql
import aiomysql


class MockHandler(tornado.web.RequestHandler):
    async def get(self, user_id):
        dummy_ids = [ random.randint(15000000, 20000000) for x in range(10) ]

        response = {
            'uid': user_id,
            'articles': dummy_ids
        }

        self.set_status(HTTPStatus.OK)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))
        self.finish()


def build_app():
    app = tornado.web.Application(
        [
            (r"/suggest/([a-z0-9]+)", MockHandler),
        ]
    )

    return app

if __name__  == "__main__":
    app = build_app()
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()
