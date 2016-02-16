import Queue
import threading
import sys

import netaddr
import nmap


class Scanner(object):
    """Multi-threaded python script to scan multiple netblocks using nmap."""
    def __init__(self, nmap_args='-T4 -F', subnets=None, threads=10):
        self.q = Queue.Queue()
        self.results = Queue.Queue()
        self.nmap_args = nmap_args
        self.threads = threads

        for subnet in subnets:
            for ipv4 in netaddr.IPNetwork(subnet):
                self.q.put(str(ipv4))

    def start(self):
        """Start workers."""
        printer = threading.Thread(target=self.printer)
        self.is_thread_alive = True
        printer.start()
        for _ in xrange(self.threads):
            worker = threading.Thread(target=self.nmap_thread)
            worker.start()
        self.q.join()
        self.is_thread_alive = False
        printer.join()
        print 'Finished scanning.'
        sys.exit(0)

    def nmap_thread(self):
        """A single thread (multi-threaded based on self.start) of the nmap
        worker."""
        while not self.q.empty():
            self.is_thread_alive = True
            ipv4 = self.q.get()
            nm = nmap.PortScanner()
            self.results.put({
                ipv4: nm.scan(hosts=ipv4, arguments=self.nmap_args)
            })
            self.q.task_done()

    def printer(self):
        while True:
            if self.results.empty() and not self.is_thread_alive:
                return
            nmap_dict = self.results.get()
            ipv4 = nmap_dict.keys()[0]
            print('[%s] Scan completed.' % (ipv4))
            self.results.task_done()
