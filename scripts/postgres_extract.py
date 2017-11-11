#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

import json
import psycopg2
import psycopg2.extras
import pymongo

from bson.json_util import dumps, loads
from django.core.serializers.json import DjangoJSONEncoder


def cursor(name=''):
    conn_string = "host='localhost' dbname='d3soppdkjvqvb0' user='peterdowns'"
    conn = psycopg2.connect(conn_string)
    c = conn.cursor('server_side_cursor_' + name, cursor_factory=psycopg2.extras.RealDictCursor)
    return c


def dump_postgres():
    print('writing documents...')
    fout = open('./documents.jsonlines', 'w')
    c = cursor('docs')
    c.execute('SELECT * FROM documents')
    for row in c:
        json.dump(row, fout, cls=DjangoJSONEncoder)
        fout.write('\n')
    fout.close()

    print('writing users...')
    fout = open('./users.jsonlines', 'w')
    c = cursor('users')
    c.execute('SELECT * FROM users')
    for row in c:
        json.dump(row, fout, cls=DjangoJSONEncoder)
        fout.write('\n')
    fout.close()


def dump_mongodb():
    print('writing annotations')
    c = pymongo.MongoClient()
    fout = open('./annotations.jsonlines', 'w')
    for row in c.test.annotations.find({}):
        fout.write(dumps(row, cls=DjangoJSONEncoder))
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    print('> executing...')
    dump_postgres()
    dump_mongodb()
    print('> done.')
