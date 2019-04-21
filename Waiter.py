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
logger = logging.getLogger('Waiter')


class Waiter(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
        self.client_req = {}
        self.clients_deliever = {}

    def check_deliver(self,ticket):
        return ticket in self.client_req and ticket in self.clients_deliever

    def run(self):
        self.node.start()
        time.sleep(3)
        t = self.node.table
        
        while True:
            o = self.node.queuein()
            if o is not None:
                ticket = o['args']['ticket']
                method = o['method']
                logger.info("{}: {}".format(method,ticket))

                if method == 'PICKUP_REQ':
                   self.client_req[ticket]=o['args']['address']    
                
                elif method == 'FOOD_READY':
                    self.clients_deliever[ticket]=o['args']['order']
                
                if self.check_deliver(ticket):
                    o={'method': 'DELIVER_READY','args':{'ticket':ticket,'order': self.clients_deliever[ticket]}}
                    self.node.send(self.client_req[ticket],o)
                    logger.info("DELIVER_READY {}: {}".format(ticket, self.clients_deliever[ticket]))
                
    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()