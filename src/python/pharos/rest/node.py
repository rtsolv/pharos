import json

import flask
from flask import request

import pymongo
from pharos.rest import *

class AlreadyExists(InvalidUsage):
    def __init__(self, record, status_code=None, payload=None):
        InvalidUsage.__init__(self, 'Already Exists: ' + repr(record), status_code, payload)


@app.route('/node', methods=['GET', 'POST'])
def list_node():
    c = pymongo.MongoClient('localhost:27017') 
    if request.method == 'POST':
        # insert new recode
        req = json.loads(request.data)
        res = c.pharos.node.find_one(req)
        if res:
            # return conflict current recode: 409
            raise AlreadyExists(res, status_code=409)
        res = c.pharos.node.insert(req)
        if not res:
            pass
        req['_id'] = str(req.pop('_id'))
        return flask.jsonify(req)

    nodes = list(c.pharos.node.find())
    res = {'n': len(nodes)}
    for node in nodes:
        node['_id'] = str(node.pop('_id'))
    res['nodes'] = nodes
    return flask.jsonify(res)

@app.route('/node/<host>/metrics', methods=['GET'])
def metrics_node(host=None):
    c = pymongo.MongoClient('localhost:27017')
    q = {'hostname': host}
    containers = list(c.pharos.metrics.find(q))
    res = {'n': len(containers)}
    for container in containers:
        container['_id'] = str(container.pop('_id'))
    
    res['containers'] = containers
    return flask.jsonify(res)
