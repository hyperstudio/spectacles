# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
import annoy
import time
import random


class Indexer(object):
    def __init__(self,
            index_path,
            update_interval=10,
            index_trees=20,
            vector_length=384):
        self.index_path = index_path
        self.update_interval = update_interval
        self.index_trees = index_trees
        self.vector_length = vector_length

        self.mapping = {}

    def initial_load(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def save_annoy_file(self):
        index = annoy.AnnoyIndex(self.vector_length)
        for i, v in self.mapping.items():
            index.add_item(i, v)
        index.build(self.index_trees)
        index.save(self.index_path)
        index.unload()

    def run(self):
        self.initial_load()
        try:
            while True:
                self.update()
                self.save_annoy_file()
                time.sleep(self.update_interval)
        except KeyboardInterrupt:
            pass


class DummyIndexer(Indexer):
    def initial_load(self):
        for i in xrange(0, 1000):
            v = [random.gauss(0, 1) for z in xrange(self.vector_length)]
            self.mapping[i] = v

    def update(self):
        changed = 0
        for i in xrange(0, 1000):
            if random.random() > 0.5:
                continue
            changed += 1
            v = [random.gauss(0, 1) for z in xrange(self.vector_length)]
            self.mapping[i] = v
        print('updated %d items' % changed)


if __name__ == '__main__':
    d = DummyIndexer(
        index_path='./dummy.ann',
        update_interval=5
    )
    d.run()
