# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from Node import Node 

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
        time.sleep(3)
        t = self.node.table
        while True:            
            o = self.node.queuein()
            if o is not None:
                if o['method'] == 'ORDER':  
                    self.node.send(o['args']['address'],{'method':'ORDER_REP','args':{'ticket':self.ticket}})
                    self.node.queueout({'id':t['CHEF'],'method':'ORDER_FOOD','args':{'order':o['args']['order'],'ticket':self.ticket}})
                    self.ticket= self.ticket+1
                elif o['method'] == 'PICKUP':
                    self.node.queueout({'id':t['WAITER'],'method':'PICKUP_REQ','args':{'ticket':o['args']['order']['ticket'],'address':o['args']['address']}})

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()

