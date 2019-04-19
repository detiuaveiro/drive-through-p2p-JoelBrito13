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
logger = logging.getLogger('Restaurant')


class Restaurant(threading.Thread):
    def __init__(self, id, address,name, successor_addr = None):
        threading.Thread.__init__(self)
        self.node = Node(id, address, name, successor_addr)


    def run(self):
        self.node.start()

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return self.__str__()
