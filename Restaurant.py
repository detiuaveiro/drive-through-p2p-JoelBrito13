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
        self.grill = Grill(average=3,desviation=0.5)
        self.fryer = Fryer(average=5,desviation=0.5)
        self.drink = Drink(average=1,desviation=0.5)

        self.grill_queue = queue.Queue()
        self.fryer_queue = queue.Queue()
        self.drink_queue = queue.Queue()

    def make_request(self):
        if self.drink.is_available() and not self.drink_queue.empty():
            self.drink.prepare()
        if self.grill.is_available() and not self.grill_queue.empty():
            self.grill.prepare()
        if self.fryer.is_available() and not self.fryer_queue.empty():
            self.fryer.prepare()

    def request_done(self):
        #sort by the lowest wait_time
        if self.drink.is_complete():
            return 'DRINK_DONE', self.drink_queue.get()
        if self.grill.is_complete():
            return 'HAMBURGER_DONE', self.grill_queue.get()

        if self.fryer.is_complete():
            return 'POTATO_DONE', self.fryer_queue.get()
        return None, None


    def run(self):
        self.node.start()
        time.sleep(3)
        t = self.node.table
        
        while True:
            o = self.node.queuein()
            if o is not None:
                method=o['method']
                ticket=o['args']['ticket']
                logger.info("{}: {}".format(method,ticket))

                if method == 'PREPARE_DRINK':
                    self.drink_queue.put(ticket)
        
                elif method == 'GRILL_HAMBURGER':
                    self.grill_queue.put(ticket)
        
                elif method == 'FRY_POTATO':
                    self.fryer_queue.put(ticket)
                            
            self.make_request()

            method, ticket = self.request_done()
            if method is not None:
                o={'id':t['CHEF'], 'method': method,'args':{'ticket': ticket}}
                logger.info("{}: {}".format(method,ticket))
                self.node.queueout(o)

    def __str__(self):
        return "{}\nDevices= {}, {}, {}".format(self.node, self.drink, self.grill, self.fryer)

    def __repr__(self):
        return self.__str__()

class Timer_Class:
    def __init__(self,average,desviation):
        self.available=True
        self.average=average
        self.desviation=desviation

    def prepare(self):
        self.start_time = time.time()
        self.time_till_ready = random.gauss(self.average,self.desviation)
        self.available = False

    def is_complete(self):
        if self.available:
            return False
        if time.time() >= self.start_time + self.time_till_ready:
            self.available=True
            return True
        return False

    def is_available(self):
        return self.available

    def __str__(self):
            return self.__class__.__name__ + ": " +str(self.average) + "segs" 

    def __repr__(self):
        return self.__str__()


class Grill(Timer_Class):
    def __init__(self,average=3,desviation=0.5):
        super().__init__(average,desviation)

class Fryer(Timer_Class) : 
    def __init__(self,average=5,desviation=0.5):
        super().__init__(average,desviation)

class Drink(Timer_Class) :
    def __init__(self,average=1,desviation=0.5):
        super().__init__(average,desviation)
