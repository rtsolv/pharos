import os, sys
import encodings.idna
import numpy
import psutil
import docker
import pymongo
import yaml

from pharos._node import Node
import pharos._mongodb as db
# TODO implement: another database or filesystem likes as db

from _common import (REMOTE_API_PORT,
                    LIGHTTOWER_PORT,
                    DOCKER_BRIDGE,
                    DOCKER_PORT,
                    DOCKER_API_VERSION,
                    MONGOS_PORT,
                    CONFIG_FIELDS)

from _common import (get_configuration,
                    get_preference)                    

_client = None

def client():
    global _client

    if not _client:
        config = get_configuration()  
        _client = PharosClient(config)
    return _client

class PharosClient(object):
    def __init__(self, config):
        self.config = config

    def get_configuration(self):
        return self.config

    def containers(self, nodes=None):
        if not nodes:
            nodes = self.nodes()
        containers = []
        for node in nodes():
            containers += node.containers()
        
        return containers

    def hosts(self):
        return db.get_hosts()

    def nodes(self):
        return [Node(host['host']) for host in self.hosts()]
    
    def get_node(self, host):
        return Node(host)

