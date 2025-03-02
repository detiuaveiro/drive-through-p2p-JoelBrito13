# coding: utf-8

import time
import pickle
import socket
import random
import logging
import argparse
import threading 
 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main(name, port, ring, timeout):
    # Create a logger for the client
    logger = logging.getLogger('Client {}'.format(name))
    
    # UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.bind(('localhost', port))

    # Generate a request
    order = {'hamburger': 0, 'fries': 0, 'drink': 0}
    quantity = random.randint(1,5)
    for i in range(quantity):
        order[random.choice(['hamburger', 'fries', 'drink'])] += 1

    # Wait for a random time
    delta = random.gauss(2, 0.5)
    logger.info('Wait for %f seconds', delta)
    time.sleep(delta)

    # Request some food
    logger.info('Request some food: %s', order)
    p = pickle.dumps({'method': 'ORDER', 'args': order})
#    p = pickle.dumps({'method': 'ORDER', 'args':{'hamburger': 1, 'fries': 0, 'drink': 0}})
    sock.sendto(p, ring)

    # Wait for Ticket
    p, addr = sock.recvfrom(1024)
    o = pickle.loads(p)
    logger.info('Received ticket %s', o['args'])

    # Pickup order 
    logger.info('Pickup order %s', o['args'])
    p = pickle.dumps({"method": 'PICKUP', "args": o['args']})
    sock.sendto(p, ring)

    # Wait for order
    p, addr = sock.recvfrom(1024)
    o = pickle.loads(p)
    logger.info('Got order %s', o['args'])

    return 0 
    #Close socket
    #thread.join()
    #socket.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pi HTTP server')
    parser.add_argument('-p', dest='port', type=int, help='client port', default=5004)
    parser.add_argument('-r', dest='ring', type=int, help='ring ports ', default=5000)
    parser.add_argument('-t', dest='timeout', type=int, help='socket timeout', default=60)
    parser.add_argument('-c', dest='clients', type=int, help='num clients ', default=3)
    args = parser.parse_args()
    
    names=['Batman','IronMan','WonderWoman','BlackWidow','Nakia','CamilaUachave','DiogoGomes','JeanBrito','MarioAntunes']
    
    for i in range(args.clients):
        client_name="{} {}".format(random.choice(names),i)
        thread = threading.Thread(target=main, args=(client_name, args.port+i, ('localhost', args.ring), args.timeout))
        thread.start()
