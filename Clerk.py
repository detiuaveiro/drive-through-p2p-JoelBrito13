# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from node import Node 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Clerk')
    

class Clerk(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
        self.ticket = 0

    def run(self):
        self.node.start()
        o = self.node.queuein()
        t = self.node.table
        v = o.get()
        if v['method'] == 'ORDER':  
            self.node.send(v['args']['address'],self.ticket)
            self.counter= self.counter+1
            self.node.queueout({'id':t['CHEF'],'method':'ORDER','args': {'order':{v['args']},'ticket':self.ticket}})
        elif v['method'] == 'PICKUP':
            self.node.queueout({'id':t['WAITER'],'method':'PICKUP','args':{'ticket':self.ticket}})

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()

