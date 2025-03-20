#!/usr/bin/env python3

import sys
import json
from urllib.request import urlopen
import socket
import os

# receice a dns to validate and convert to an ip address
def convert_dns_to_ip(dns):
	try:
		return socket.gethostbyname(dns)
	except socket.gaierror as e:
		print("Invalid address!")
		sys.exit(1)

# receive a ip address and get informations from via ipinfo.io
def geoip(ip_addr):
	url = 'http://ipinfo.io/'+ ip_addr + '/json'
	response = urlopen(url)
	data = json.load(response)
	return data

# receive a json and transform to a string easy to read
def geoip_toString(data):
	res = ""
	for d in data:
		res += (str(d) + ": " + str(data[d]) + "\n")
	return res

# execute functions step by step until print to terminal
def execute_geoip(data):
	ip_addr = convert_dns_to_ip(data)
	data = geoip(ip_addr)
	string_data = geoip_toString(data)
	print(string_data)

# read a file to execute a multiple consults at one time
def get_from_file():
	abspath = os.path.abspath(os.getcwd())
	txtfile = abspath + '/domains.txt'
	with open(txtfile, 'r') as file:
		for line in file:
			line = line.strip()
			print(line)
			execute_geoip(line)
			print('\n------------------\n')

def main():
	# if program have parameters passed via terminal
	if len(sys.argv) > 1:
		# if parameter '-f' will read from the file
		if sys.argv[1] == '-f': 
			print('Trying to read file domains.txt...')
			try:
				# try to read the domains.txt file
				get_from_file()
			except Exception as e:
				# if file doesnt exist raise an exception
				print(e)
			# stops main function here
			return
		
		# else paremeter is not '-f' execute function with parameter passed via terminal
		execute_geoip(sys.argv[1])

if __name__ == '__main__':
	main()
