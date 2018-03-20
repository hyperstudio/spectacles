#!/bin/bash
set -e
nohup ./daemons/annotation_indexer.py &
nohup ./daemons/annotation_server.py &
nohup ./daemons/document_indexer.py &
nohup ./daemons/document_server.py &
