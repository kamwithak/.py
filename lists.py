#!/usr/bin/python

import sys

def search(array, prompt):

	print "Which element (@ specific byte) would you like to print within the list (0 - 5) (-1 = EXIT):",
	i = int(raw_input())

	if i == -1:
		
		sys.exit(0)

	elif i > 5 or i < 0:

		print '\n', prompt, "ERROR - STAY WITHIN RANGE OF LIST", '\n'
		search(array, prompt)                                                           

	else:

		selected_element = array[i]
		print '\n', prompt, selected_element, '\n'
		search(array, prompt)

if __name__ == "__main__":

	i = 0
	e = "Empty"
	c = "Current"
	prompt = ' -> '
	array = [] #empty array

	#build a mechanism that asks how many elements and make a while loop for that, using true and false prefered

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
	search(array, prompt)

