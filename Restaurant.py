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
logger = logging.getLogger('Restaurant')


class Restaurant(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
        self.hamburger = Grill()
        self.fries = Fryer()
        self.drink = Drink()

    
    
    def run(self):
        self.node.start()
        time.sleep(3)
        t = self.node.table
        while True:
            o = self.node.queuein()
            if o is not None:
                if o['method'] == 'GRILL_HAMBURGER':
                    g = grill()
                    if g.ready():
                       self.node.queueout({'id':t['CHEF'],'method': 'HAMBURGER_DONE','args':{'ticket': o['args']['ticket']}})
                elif o['method'] == 'PREPARE_DRINK':
                    g = grill()
                    if g.ready():
                       self.node.queueout({'id':t['CHEF'],'method': 'DRINK_DONE','args':{'ticket': o['args']['ticket']}})
                if o['method'] == 'FRY_POTATO':
                    g = grill()
                    if g.ready():
                       self.node.queueout({'id':t['CHEF'],'method': 'POTATO_DONE','args':{'ticket': o['args']['ticket']}})

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()

class Grill:
    def __init__(self,average=3,desviation=0.5):
        self.average = average
        self.desviation = desviation
    def ready (self):
        delta = random.gauss(self.average, self.desviation)
        start_time = time.time()
        if time.time() > stat_time+delta:
            return True
            
class Fryer : 
    def __init__(self,average=5,desviation=0.5):
        self.average = average
        self.desviation = desviation
    def ready (self):
        delta = random.gauss(self.average, self.desviation)
        start_time = time.time()
        if time.time() > stat_time+delta:
            return True

class Drink :
    def __init__(self,average=1,desviation=0.5):
        self.average = average
        self.desviation = desviation
    def ready (self):
        delta = random.gauss(self.average, self.desviation)
        start_time = time.time()
        if time.time() > stat_time+delta:
            return True