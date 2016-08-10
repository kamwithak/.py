#!/usr/bin/python
#works with python 2.7

import sys

def search(array):

	print "Which element would you like to print within the list (0 - 5): ",
	i = int(raw_input())

	if i > 5 or i < 0:
		
		sys.exit()

	selected_element = array[i]
	print '\n', selected_element, '\n'

	search(array)

if __name__ == '__main__':

	i = 0
	e = "Empty"
	c = "Current"
	array = [] #empty array

	while i < 6:

		if i == 0:

			print "\n%s List: " % e, array

		else:

			print "\n%s List: " % c, array


		print "@ specific byte: %d" % i
		x = raw_input("Enter string: ")
		array.append(x)

		i += 1

	print "\nFinal list: ", array, "\n"

	search(array)

