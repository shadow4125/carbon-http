# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

import threading
import socket
import pickle
import struct
import time

from qg.core import log as logging

LOG = logging.getLogger(__name__)


class CarbonSender(threading.Thread):

    def __init__(self, queue, host, port, timeout=10):
        super(CarbonSender, self).__init__()

        self.queue = queue
        self.host = host
        self.port = port        # carbon pickle
        self.timeout = timeout
        self.is_running = True
        self.interval = 3
        self.send_size = 100    # should lower than CONF.queue.maxsize
        self.send_time = time.time()

        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)

        if self.sock is not None:
            LOG.debug("Attempting to connect to %s:%s" % (self.host, self.port))
            self.sock.connect((self.host, self.port))
        else:
            raise IOError("Connect to %s:%s error" % (self.host, self.port))

    def pickled(self, tuples):
        payload = pickle.dumps(tuples)
        header = struct.pack("!L", len(payload))
        return header + payload

    def send(self, data):
        try:
            if self.sock is None:
                self.connect()

            if self.sock is not None:
                LOG.debug("Sending data...")
                self.sock.sendall(data)
            else:
                LOG.error("Socket unavailable.")
        except Exception as e:
            LOG.error("Send failed %s" % str(e))
            self.close()
            raise e

    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def oversize(self):
        return (self.queue.qsize() >= self.send_size)

    def overtime(self):
        return ((time.time() - self.send_time) >= self.interval)

    def run(self):
        while self.is_running:
            # oversize or overtime
            if self.oversize() or (self.overtime() and not self.queue.empty()):
                data = []
                while len(data) < self.send_size and not self.queue.empty():
                    try:
                        data.append(self.queue.get(block=True, timeout=1))
                    except Exception as e:
                        LOG.error('Get metric from queue error :%s' % str(e))

                if len(data) > 0:
                    try:
                        self.send(self.pickled(data))
                        self.send_time = time.time()
                    except Exception as e:
                        LOG.error("Sending error: %s" % str(e))

            time.sleep(self.interval)
