import psycopg2
import os
from psycopg2 import pool, sql

from datetime import datetime

class DBModel:
    __instance = None

    def __init__(self):
        if DBModel.__instance != None:
            print("ERROR")
            pass
        else:
            postgres_config = {
                'user': os.getenv('POSTGRES_USER'),
                'password': os.getenv('POSTGRES_PASSWORD'),
                'host': os.getenv('POSTGRES_HOST')
            }

            pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=4,
                maxconn=20,
                user=postgres_config['user'],
                password=postgres_config['password'],
                host=postgres_config['host'],
                dbname='transportation'
            )
            self.pool = pool
            DBModel.__instance = self

    @staticmethod
    def getInstance():
        if DBModel.__instance == None:
            DBModel()
        return DBModel.__instance

    def run(self, query_params):
        try:
            [query, params, formatter] = query_params
        except:
            [query, params] = query_params
            formatter = None
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                cur.execute(query, params)
                # print(cur.query.decode('CP857'))
                result = cur.fetchall()
                cur.close()
        finally:
            self.pool.putconn(conn)
        if formatter:
            return formatter(result)
        return result
