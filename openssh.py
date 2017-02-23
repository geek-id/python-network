#!/usr/bin/python3

from subprocess import PIPE, call, Popen
import os, sys
from time import sleep
import re
import fileinput

DN = open(os.devnull, 'w')

# package = raw_input('Search Package : ')
# package = ['apache2', 'php', 'php-gd', 'php-mysql', 'phpmyadmin', 'mysql-server', 'mysql-client']
openssh = b'^openssh-server'
# pkg = " ".join('%s' % pkg for pkg in package)
# print pkg

def search(pkg):
	proc = Popen(['apt-cache', 'search', pkg],stdout=PIPE, stderr=DN)

	listPkg = proc.communicate()[0].split(b'\n')
	# print(listPkg)

	for package in listPkg:
		if len(package) == 0:
			continue
		if (package[0]) != b' '[0]:
			global getPackage
			getPackage = package[:package.find(b' ')]
			if re.match(pkg, getPackage, re.IGNORECASE):
				# package = getPackage
				print('Package %s available to install...' % (getPackage.decode("utf-8")))
				# install(pkg)
			else:
				print('Package %s not available, please add another repository package...' % (getPackage))
	# search_line = proc.stdout.readlines()
	# for line in search_line:
		# print line.find('openssh')
		# sleep(1)
	return getPackage

def configSSH():
	'''
		Function of configuration OpenSSH-Server
	'''

	os.system('clear')
	print('Installation Process Done...')
	print('Configuration OpenSSH-Server\n')
	configFile = '/etc/ssh/sshd_config'
	if os.path.isfile(configFile) and os.access(configFile, os.R_OK):
		# code here
		try:
	        # config = open(configFile, 'r')
			with open(configFile, 'r') as searchconfig:
				for port in searchconfig:
					if 'Port' in port:
						old_port = port
				# for rootlogin in searchconfig:
				# 	if 'PermitRootLogin' in root_login:
				# 		root_access = root_login

	        # print(root_access)

			with fileinput.FileInput(configFile, inplace=True, backup='.bak') as conf:
				new_port = input('Set Port SSH(default Port 22): ')
				default = '22'

				for configPort in conf:
						if not new_port:
							print(configPort.replace(old_port, ('Port %s\n' % default)), end="")
						else:
							print(configPort.replace(old_port, ('Port %s\n' % new_port)), end="")
			conf.close()
		except IOError:
			print('Something wrong')
	# else:
	# 	return search(openssh)

if __name__ == '__main__':
	try:
		if not os.geteuid() == 0:
			exit('Please run as r00t...\n')

		# checkPkg(openssh)

		search(openssh)

		char = re.sub(b'[\^]', b'', openssh)
		if getPackage == char:
			doInstall = call(['apt-get', 'install', getPackage], stderr=DN)
			configSSH()
			print('Configuration Success...')
			# print(getPackage.decode("utf-8"))
	except SyntaxError as error:
		print('Something wrong to execution')
