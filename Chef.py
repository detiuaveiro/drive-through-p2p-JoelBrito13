# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
import node from node 
 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('Chef')


class Chef(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)
		self.id = id
		self.adress = address
		self.ring = ring
		self.deliever_order = {}
		self.recv_orders = {}
		self.table={'RECEPCIONIST':1,'CHEF':None,'RESTAURANT':None,'WAITER':None}

    

    def run(self):
    	counter = False
        self.node.start()
		o = self.node.queuein()
		t = self.node.table
        v = o.get()
        
        if v['method'] == 'ORDER':
        	self.recv_orders[v['args']['ticket']] = v['args']['order']
        	for key in self.recv_orders[ticket]:	
    	  		self.deliever_orders[ticket][key]=0
        	if v['args']['order']['hamburguer'] is not None:
        	   self.node.queueout({'id':t['RESTAURANT'],'method':'GRILL_HAMBURGER','args':'ticket':self.ticket}})
        	elif v['args']['order']['drink'] is not None:
            	 self.node.queueout({'id':t['RESTAURANT'],'method':'PREPARE_DRINK','args':'ticket':self.ticket}})
        	elif v['args']['order']['friedPotato'] is not None:	
        		 self.node.queueout({'id':t['RESTAURANT'],'method':'FRY_POTATO','args':'ticket':self.ticket}})
        elif v['method'] == 'HAMBURGER_DONE':
        	  self.deliever_orders[v['args']['ticket']]['hamburger']=self.deliever_orders[v['args']['ticket']]['hamburger']+1
        	  counter = True
        elif v['method'] == 'DRINK_DONE':
              self.deliever_orders[v['args']['ticket']]['drink']=self.deliever_orders[v['args']['ticket']]['drink']+1
              counter = True
        elif v['method'] == 'POTATO_DONE':
              self.deliever_orders[v['args']['ticket']]['potato']=self.deliever_orders[v['args']['ticket']]['potato']+1
              counter = True
        
        if counter = True :
        	delivery = True
	        for key in self.recv_orders[v['args']['ticket']]:
	        	if not self.deliever_orders[v['args']['ticket']][key]==self.recv_orders[v['args']['ticket']][key]:
	            	delivery = False
	        self.node.queueout('id': t['WAITER'], method : 'FOOD_READY', 'args': ticket)       	





        pass

