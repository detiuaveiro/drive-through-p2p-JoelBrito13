# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from node  import Node
 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
        self.deliever_order = {}
        self.recv_orders = {}
        
    

    def run(self):
        counter = False
        self.node.start()
        o = self.node.queuein()
        t = self.node.table
        if o is not None:
            if o['method'] == 'ORDER':
                self.recv_orders[o['args']['ticket']] = o['args']['order']
                for key in self.recv_orders[ticket]:    
                    self.deliever_orders[ticket][key]=0
                if o['args']['order']['hamburguer'] is not None:
                   self.node.queueout({'id':t['RESTAURANT'],'method':'GRILL_HAMBURGER','args':{'ticket':self.ticket}})
                elif o['args']['order']['drink'] is not None:
                     self.node.queueout({'id':t['RESTAURANT'],'method':'PREPARE_DRINK','args':{'ticket':self.ticket}})
                elif o['args']['order']['friedPotato'] is not None: 
                     self.node.queueout({'id':t['RESTAURANT'],'method':'FRY_POTATO','args':{'ticket':self.ticket}})
            elif o['method'] == 'HAMBURGER_DONE':
                  self.deliever_orders[o['args']['ticket']]['hamburger']=self.deliever_orders[o['args']['ticket']]['hamburger']+1
                  counter = True
            elif o['method'] == 'DRINK_DONE':
                  self.deliever_orders[o['args']['ticket']]['drink']=self.deliever_orders[o['args']['ticket']]['drink']+1
                  counter = True
            elif o['method'] == 'POTATO_DONE':
                  self.deliever_orders[o['args']['ticket']]['potato']=self.deliever_orders[o['args']['ticket']]['potato']+1
                  counter = True
            
            if counter == True :
                delivery = True
                for key in self.recv_orders[o['args']['ticket']]:
                    if not self.deliever_orders[o['args']['ticket']][key]==self.recv_orders[o['args']['ticket']][key]:
                        delivery = False
                self.node.queueout({'id': t['WAITER'], 'method' : 'FOOD_READY', 'args':{'ticket': ticket}})        

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()
