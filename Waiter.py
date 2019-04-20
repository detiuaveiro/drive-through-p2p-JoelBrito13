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
        self.deliver = []

    def check_deliver(self,ticket):
        if ticket in self.deliver:
            self.deliver.remove(ticket)
            return True
        else:
            self.deliver.append(ticket)
        return False

    def run(self):
        self.node.start()
        time.sleep(3)
        while True:
            o = self.node.queuein()
            if o is not None:
                if o['method'] == 'DELIVER_ORDER':
                   if self.check_deliver(o['args']['ticket']):
                       logger.info('Delivering the food...%s')
                       logger.info('Payment receiving from client %s', o['args']['ticket'])
                elif o['method'] == 'PICKUP':
                   if self.check_deliver(o['args']['ticket']):
                       logger.info('Delivering the food...%s')
                       logger.info('Payment receiving from client %s', o['args']['ticket'])
    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()