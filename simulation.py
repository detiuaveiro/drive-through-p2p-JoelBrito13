# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse

from Restaurant import Restaurant
from Waiter import Waiter
from Chef import Chef
from Clerk import Clerk

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main():

logger = logging.getLogger('RESTAURANT_RING')
    ring_list=[]
    # list with all the nodes
    #self, id, address, request, successor_addr=None
    restaurant   = Restaurant  (id=0,address = ('localhost', 5000), name = 'RESTAURANT') 
    receptionist = Receptionist(id=1,address = ('localhost', 5001), name = 'RECEPCIONIST', successor_addr= ('localhost', 5000))
    chef         = Chef        (id=2,address = ('localhost', 5002), name = 'CHEF', successor_addr= ('localhost', 5000))
    waiter       = Waiter      (id=3,address = ('localhost', 5003), name = 'WAITER', successor_addr= ('localhost', 5000))

    restaurant.start()
    ring_list.append(restaurant)
    logger.info(restaurant)

    receptionist.start()
    ring_list.append(receptionist)
    logger.info(receptionist)

    chef.start()
    ring_list.append(chef)
    logger.info(chef)

    waiter.start()
    ring_list.append(waiter)
    logger.info(waiter)

    
    # Await for ring to get stable
    time.sleep(10)

    for node in ring_list:
        node.join()

if __name__ == "__main__":
    main()