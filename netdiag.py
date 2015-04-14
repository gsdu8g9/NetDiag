import netaddr
import argparse
import os
import Queue
import socket
import subprocess
import sys
import threading


HOSTS = []

class autobot(object):
	def __init__(self, subnet):
		self.q = Queue.Queue()
		self.subnet = subnet

	def _subnet_to_ips(self):
		args = parse_arguments()
		netblock = netaddr.IPNetwork(self.subnet)

		self.q = Queue.Queue()
		for ipaddr in netblock:
			self.q.put(ipaddr)

		for _ in xrange(args.threads):
			worker = threading.Thread(target=ping, args=(q,))
			worker.setDaemon(True)
			worker.start()
		self.q.join()

	def ping(self):
		while True:
			ipaddr = self.q.get()
			FNULL = open(os.devnull, 'w')
			response = subprocess.call(
				["ping","-c","1","%s" % ipaddr],
				stdout=FNULL)
			if response == 0:
				HOSTS.append(ipaddr)
			self.q.task_done()
		if len(HOSTS) > 0:
			print("The following hosts are alive:")
			for host in HOSTS:
				print("\t[+] %s" % host)

	def dns(self):
		while True:
			ipaddr = self.q.get()
			try:
				results = socket.gethostbyaddr(ipaddr)
				hostname = 
			except socket.herror:

			self.q.task_done()


def parse_arguments():
	"""Parse arguments"""
	parser = argparse.ArgumentParser(
		description="Ping sweep for hosts and better help determining subnets.")
	parser.add_argument(
		"--subnet",
		type=str,
		required=True,
		help="Subnet block that you would like to scan.")
	parser.add_argument(
		"--threads",
		type=int,
		default=20,
		help="Count of threads that you would like to use.")
	parser.add_argument(
		"--ping",
		action=store_true,
		help="Ping sweept the subnet.")
	parser.add_argument(
		"--dns",
		action=store_true,
		help="Reverse DNS lookup on the subnet.")
	return parser.parse_args()


def main():
	"""Main function"""
	args = parse_arguments()
	sweep = autobot(args.subnet)
	
	if not args.ping and not args.dns:
		print('Ping and or DNS was not selected.')
		sys.exit()
	if args.ping:
		sweep.ping()
	if args.dns:
		sweep.dns()


if __name__ == "__main__":
	main()
