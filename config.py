import os
import sys

DB_config = {
    'host': os.environ['dbhost'],#'news-recommendation.cvynbgusgzyb.ap-northeast-2.rds.amazonaws.com',
    'port': os.environ['dbport'],
    'user':os.environ['dbusr'],
    'password': os.environ['dbpwd'],
    'db' : 'innodb'
}

recommender_config = {
    'time_divider': 3600 * 24
}
