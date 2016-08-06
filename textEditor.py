#!/usr/bin/python
#works with python 2.7

import sys 
from sys import argv

def fetchFile(filename):

	d = input("\nEdit file = 1  View file = 2\n -> ")
	
	if d == 1:
		txt = open(filename, 'w')
		txt.truncate()
		msg = raw_input("\nWhat would you like to enter in the file:\n -> ")
		txt.write(msg)
		txt.close()
		fetchFile(filename)
	elif d == 2:
		txt = open(filename, 'r')
		i = txt.read()
		print "\nFile Content\n------------\n" + i
		txt.close()
		fetchFile(filename)
	else: sys.exit()

def menu(repo, filename):

	if repo == 'y' or repo == 'Y':
		fetchFile(filename)
	elif repo == 'n' or repo == 'N':
		print "\nExiting!"
		sys.exit()
	else:
		print "\nError, restart Text editor!"
		sys.exit()

def init(script, user, filename, prompt):

	print "\nHi %s, this is the %s script!" % (user, script)
	print "Today we will alter the selected file: %s" % filename

	print "\nProceed to main menu? y/n\n",
	repo = raw_input(prompt)
	
	menu(repo, filename)

if __name__ == '__main__':

	script, user, filename = argv  #python textEditor.py David file.txt
	prompt = ' -> '
	
	init(script, user, filename, prompt)

