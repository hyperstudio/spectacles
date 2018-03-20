#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
import time
import random
import numpy as np
import annoy
from pyRpc import PyRpc
import logging


class Server(object):
    def __init__(self,
            index_path,
            service_name,
            num_workers=8,
            update_interval=5,
            vector_length=384,
            logging_level=None):
        self.index_path = index_path
        self.service_name = service_name
        self.num_workers = num_workers
        self.update_interval = update_interval
        self.vector_length = vector_length
        if logging_level is not None:
            logging.basicConfig(level=logging_level)

        self.index = annoy.AnnoyIndex(self.vector_length)

    def neighbors_by_vector(self, vector, n, *args, **kwargs):
        return self.index.get_nns_by_vector(
                vector, n, *args, **kwargs)

    def neighbors_by_id(self, id, n, *args, **kwargs):
        return self.index.get_nns_by_item(
                id, n, *args, **kwargs)

    def num_items(self):
        return self.index.get_n_items()

    def run(self):
        server = PyRpc(self.service_name, workers=self.num_workers)
        server.publishService(self.neighbors_by_vector)
        server.publishService(self.neighbors_by_id)
        server.publishService(self.num_items)
        server.start()
        try:
            while True:
                time.sleep(self.update_interval)
                try:
                    new_index = annoy.AnnoyIndex(self.vector_length)
                    new_index.load(self.index_path)
                    self.index.unload()
                    self.index = new_index
                except IOError:
                    print('could not reload', self.index_path)
        except KeyboardInterrupt:
            server.stop()
