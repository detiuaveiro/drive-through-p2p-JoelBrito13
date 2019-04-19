# coding: utf-8
import random
import socket
import threading
import logging
import pickle
from utils import *
import queue

import time


class Node(threading.Thread):
    def __init__(self, id, address, name, successor_addr, timeout=1):
        threading.Thread.__init__(self)
        self.id = id
        self.address = address
        self.name=name
        self.successor_id = 0
        self.queue = queue.Queue()
        self.table = {'RECEPCIONIST':None,'CHEF':None,'RESTAURANT':None,'WAITER':None}
        self.table[self.name]=self.id
        self.discovered=False
        
        if successor_addr is None:
            self.successor_addr = address
            self.inside_ring = True

        else:
            self.successor_addr = successor_addr
            self.inside_ring = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self.logger = logging.getLogger("Node {}: {}".format(self.name, self.id))

    def send(self, address, o):
        p = pickle.dumps(o)
        self.socket.sendto(p, address)

    def recv(self):
        try:
            p, addr = self.socket.recvfrom(1024)
        except socket.timeout:
            return None, None
        else:
            if len(p) == 0:
                return None, addr
            else:
                return p, addr
                

    def queuein(self):
        return {}

    def queueout(self):
        return {}        


    def discover(self, args):
        temp_table = args['table']
        for key in temp_table:
            if temp_table[key] and not self.table[key]:
                self.table[key]=temp_table[key]
        if not [x for x in self.table if not self.table[x]]:
            self.discovered=True
            self.logger.info(self)
        return {'method':'NODE_DISCOVERY', 'args':{'table':self.table}}

    def run(self):
        self.socket.bind(self.address)
        while True:
            self.logger.info(self)
            if not self.inside_ring:
                #time.sleep(int(random.random()*5)

                o = {'method': 'JOIN_REQ', 'args': {'id':self.id, 'address':self.address}}
                self.send(self.successor_addr, o)
            #elif not self.discovered:
            #    o = { 'method':'NODE_DISCOVERY', 'args':{'table':self.table}}
            #    self.send(self.successor_addr, o)
            p, addr = self.recv()
            if p is not None:
                o = pickle.loads(p)
                args=o['args']
                self.logger.info('O: %s', o)
                if o['method'] == 'JOIN_REQ':
                    if contains_successor(self_id=self.id, successor_id=args['id']):
                        self.successor_addr = args['address']
                        self.successor_id = args['id']
                        o={'id':self.successor_id, 'method':'JOIN_REP', 'args':{}}
                    self.send(self.successor_addr, o)

                elif o['method'] == 'NODE_DISCOVERY':
                    o = self.discover(args)
                
                elif o['id']==self.id:
                    if o['method'] == 'JOIN_REP':
                        self.inside_ring = True
                        
#                    self.queuein({'method':o['method'],'args':o['args']})
                    #else:
#                        self.queuein(o['method'],o['args'])
                #elif o['id'] == None:
                #    if not self.queue_out.empty():#or timeout
                #        o=self.queue_out.get()
                else:
                    self.send(self.successor_addr, o)
                


    def __str__(self):
        return 'Node {}: id:{} Successor: {}:{}'.format(self.name, self.id, self.successor_id, self.successor_addr[1])

    def __repr__(self):
        return self.__str__()
