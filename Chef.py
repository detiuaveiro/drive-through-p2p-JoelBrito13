# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from Node  import Node
 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
        self.deliever_orders = {}
        self.recv_orders = {}    

    def run(self):
        self.node.start()
        time.sleep(3)
        counter = False 
        t=self.node.table
               
        while True:
            o = self.node.queuein()
            if o is not None:

                ticket=o['args']['ticket']
                method=o['method']
                
                if method == 'ORDER_FOOD':
                    orders=o['args']['order']
                    self.recv_orders[ticket] = orders
                    self.deliever_orders[ticket]={}

                    for key in self.recv_orders[ticket]:
                        self.deliever_orders[ticket][key]=0

                    random_req=[]  

                    for x in range(orders['hamburger']):
                        random_req.append({'id':t['RESTAURANT'],'method':'GRILL_HAMBURGER','args':{'ticket':ticket}} )
                    for x in range(orders['drink']):
                        random_req.append({'id':t['RESTAURANT'],'method':'PREPARE_DRINK','args':{'ticket':ticket}})
                    for x in range(orders['fries']):
                        random_req.append({'id':t['RESTAURANT'],'method':'FRY_POTATO','args':{'ticket':ticket}})

                    random.shuffle(random_req) #generate random requests

                    for x in random_req:
                        self.node.queueout(x)
                        logger.info("{}: {}".format(x['method'],ticket))

                else:
                    logger.info("{}: {}".format(method, ticket))
                    if method == 'HAMBURGER_DONE':
                          self.deliever_orders[ticket]['hamburger']=self.deliever_orders[ticket]['hamburger']+1
                    elif method == 'DRINK_DONE':
                          self.deliever_orders[ticket]['drink']=self.deliever_orders[ticket]['drink']+1
                    elif method == 'POTATO_DONE':
                          self.deliever_orders[ticket]['fries']=self.deliever_orders[ticket]['fries']+1
                    
                    delivery = True
                    for key in self.recv_orders[ticket]:
                        if not self.deliever_orders[ticket][key]==self.recv_orders[ticket][key]:
                            delivery = False
                    if delivery:
                        o={'id': t['WAITER'], 'method': 'FOOD_READY', 'args':{'ticket': ticket,'order': self.deliever_orders[ticket]}}
                        logger.info("FOOD_READY {}: {}".format( ticket, self.deliever_orders[ticket]))
                        self.node.queueout(o)

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()


