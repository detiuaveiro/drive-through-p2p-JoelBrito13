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
        self.queue_in = queue.Queue()
        self.queue_out = queue.Queue()
        self.table = {'RESTAURANT':None,'CLERK':None,'CHEF':None,'WAITER':None}
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
        if self.queue_in.empty():
            return None
        return self.queue_in.get()

    def queueout(self,o):
        self.queue_out.put(o)
                
    def discover(self, table, discovered_table):
        for key in table:
            if not table[key] == None and self.table[key] == None:
                self.table[key]=table[key]
        if not self.discovered and not [x for x in self.table if self.table[x] == None]:#check if table is complete
            self.discovered=True
            self.logger.debug('Discovered all entities-> {}'.format(self.table))       
        discovered_table[self.id] = self.discovered
        if check_lst_true(lst=discovered_table): #utils
            return None

        return {'id':self.successor_id, 'method':'NODE_DISCOVERY', 'args':{'table':self.table,'discovered_table':discovered_table}}

    def run(self):
        self.socket.bind(self.address)
        send_discover = True
        first_msg = True
            
        if self.inside_ring:
            self.logger.debug('Joined the ring')
        
        while True:

            if not self.inside_ring:
                o = {'method': 'NODE_JOIN', 'args': {'id':self.id, 'address':self.address}}
                self.send(self.successor_addr, o)
                
                #just need to be sendeed one time by the last node to join the ring
                
            elif send_discover: 
                o = {'id': self.successor_id, 'method':'NODE_DISCOVERY', 'args':{'table':self.table,'discovered_table':[False]*4}}
                self.send(self.successor_addr, o)
                send_discover=False

            p, addr = self.recv()
            if p is not None:
                o = pickle.loads(p)
                args = o['args']
                method = o['method']
                
                #uncomment to see all the msgs
                #self.logger.info('O: {}'.format(o))
                
                if not 'id' in o:
                    if method == 'NODE_JOIN':
                        if contains_successor(self_id=self.id, successor_id=args['id']):
                            self.successor_addr = args['address']
                            self.successor_id = args['id']
                            o={'id':self.successor_id, 'method':'JOIN_REP', 'args':{}}

                        self.send(self.successor_addr, o)
                    else: #msg from the client
                        t={}
                        t['order']=args
                        t['address']=addr
                        o = {'id':self.table['CLERK'],'method': method, 'args': t}
                        if first_msg:   #make sure there are only one msg on the ring
                            self.send(self.successor_addr, o)
                            first_msg=False
                        else:
                            self.queue_out.put(o)
                else:
                    id = o['id']
                    if id == self.id:
                       
                        if method == 'JOIN_REP':
                            self.logger.debug('Joined the ring')
                            self.inside_ring = True

                        #make sure the msg stops after everyone complete their tables
                        elif method == 'NODE_DISCOVERY':
                            o = self.discover(table = args['table'], discovered_table=args['discovered_table'])
                            if o is not None:
                                self.send(self.successor_addr, o)
                        else:
                            self.queue_in.put({'method':method,'args':args})
                            if not self.queue_out.empty():
                                o = self.queue_out.get()
                            else:
                                o = {'id':None,'method':None,'args':None}
                            self.send(self.successor_addr, o)
     
                    elif id == None:
                        if not self.queue_out.empty():
                            o = self.queue_out.get()
                        self.send(self.successor_addr, o)
                    else:
                        self.send(self.successor_addr, o)
                    
    def __str__(self):
        return 'Successor: {} InsideRing: {} Table: {}'.format( self.successor_id,self.inside_ring, self.table)

    def __repr__(self):
        return self.__str__()
