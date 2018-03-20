# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals
import annoy
import time
import pdb
import tqdm
import random
import multiprocessing


def graceful_exit(fn):
    def _impl(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            return None
    return _impl


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
        # Return Falsey if no updates were detected
        raise NotImplementedError

    def save_annoy_file(self):
        index = annoy.AnnoyIndex(self.vector_length)
        for i, v in tqdm.tqdm(self.mapping.items()):
            try:
                index.add_item(i, v)
            except IndexError as e:
                print('failed to add index i =', i, e, v)
                pdb.set_trace()
                continue
        t = time.time()
        index.build(self.index_trees)
        index.save(self.index_path)
        print('built and saved index:', time.time() - t)
        index.unload()

    def _run_init(self):
        self.initial_load()
        self.save_annoy_file()

    def _run_step(self):
        changed = self.update()
        if changed:
            self.save_annoy_file()

    @graceful_exit
    def run(self):
        self._run_init()
        while True:
            self._run_step()
            time.sleep(self.update_interval)

    def background(self):
        p = multiprocessing.Process(target=self.run, args=tuple())
        p.daemon = False
        p.start()
        return p
