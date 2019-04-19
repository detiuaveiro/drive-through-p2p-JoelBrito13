# coding: utf-8
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
        self.table = {'RESTAURANT':None,'CLERK':None,'CHEF':None,'WAITER':None}
        self.table[self.name]=self.id
        self.discovered=False
        self.all_discovered=False
        
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

    def discover(self, table, discovered_table):
        for key in table:
            if not table[key] == None and self.table[key] == None:
                self.table[key]=table[key]
        if not self.discovered and not [x for x in self.table if self.table[x] == None]:#check if table is complete
            self.discovered=True
            self.logger.debug('Discovered all entities-> {}'.format(self.table))
        
        discovered_table[self.id] = self.discovered

        if check_lst_true(lst=discovered_table): #utils
            self.all_discovered=True
            return None

        return {'id':self.successor_id, 'method':'NODE_DISCOVERY', 'args':{'table':self.table,'discovered_table':discovered_table}}

    def run(self):
        self.socket.bind(self.address)
        send_discover=True
        while True:
            #self.logger.info(self)
            if not self.inside_ring:
                o = {'method': 'JOIN_REQ', 'args': {'id':self.id, 'address':self.address}}
                self.send(self.successor_addr, o)

            elif send_discover: #just need to be sendeed one time
                o = {'id': self.successor_id, 'method':'NODE_DISCOVERY', 'args':{'table':self.table,'discovered_table':[False]*4}}
                self.send(self.successor_addr, o)
                send_discover=False

            p, addr = self.recv()
            if p is not None:
                o = pickle.loads(p)
                args=o['args']
                self.logger.info('O: {}'.format(o))
                if o['method'] == 'JOIN_REQ':
                    if contains_successor(self_id=self.id, successor_id=args['id']):
                        self.successor_addr = args['address']
                        self.successor_id = args['id']
                        o={'id':self.successor_id, 'method':'JOIN_REP', 'args':{}}
                    self.send(self.successor_addr, o)

                elif o['id']==self.id:
                    if o['method'] == 'JOIN_REP':
                        self.logger.debug('Joined the ring')
                        self.inside_ring = True

                    elif o['method'] == 'NODE_DISCOVERY' and not self.all_discovered:
                        o = self.discover(table = args['table'], discovered_table=args['discovered_table'])
                        if o is not None:
                            self.send(self.successor_addr, o)
                    
                            
#                    self.queuein({'method':o['method'],'args':o['args']})
                    #else:
#                        self.queuein(o['method'],o['args'])
                #elif o['id'] == None:
                #    if not self.queue_out.empty():#or timeout
                #        o=self.queue_out.get()
                else:
                    self.send(self.successor_addr, o)
                


    def __str__(self):
        return 'Successor: {} InsideRing: {} Table: {}'.format( self.successor_id,self.inside_ring, self.table)

    def __repr__(self):
        return self.__str__()
