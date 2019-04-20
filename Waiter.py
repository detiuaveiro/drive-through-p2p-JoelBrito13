# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading
import queue
from node import Node 

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
		o = self.node.queuein()
		d = self.node.deliver
		v = o.get()
   
		if v['method'] == 'DELIVER_ORDER':
		   if self.check_deliver(v['args']['ticket']):
		   	   logger.info('Delivering the food...%s')
		   	   logger.info('Payment receiving from client %s', v['args']['ticket'])
		elif v['method'] == 'PICKUP':
		   if self.check_deliver(v['args']['ticket']):
		   	   logger.info('Delivering the food...%s')
		   	   logger.info('Payment receiving from client %s', v['args']['ticket'])


		pass