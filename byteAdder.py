def _and_(i, j):
	return (i and j)
def _or_(i, j):
	return (i or j)
def _not_(i):
	return (not i)
def _xor_(i, j):
	return (_or_(_and_(i,_not_(j)),_and_(_not_(i),j)))
def _if_(i, j):
	return (_or_(_not_(i), j))
def _iff_(i, j):
	return (_and_(_or_(_not_(i), j),_or_(i, _not_(j))))

def WhatIsTheNameOfMyComputer():
	return None

import sys

arr = [] ; byte1Boolean = [] ; byte2Boolean = [] # memory for full-adder algorithm
s = False ; c = False ; k = 0 # variables (these change)
MAX_BITS = 8 ; T = True ; F = False # constants (these don't change)

def full_Adder(x, y, z_carry):
	def half_Adder(x, y):
		s = _xor_(x, y)
		c = _and_(x, y)
		return s, c

	s1, c1 = half_Adder(x, y)
	s2, c2 = half_Adder(s1, z_carry)
	return s2, _or_(c1, c2)

def byte_Adder(str1, str2):
	global byte1Boolean, byte2Boolean, arr, k, s, c
	byte1 = map(int, list(str1)) ; byte2 = map(int, list(str2)) # conversion to int-type

	for i in byte1:
		if i is int(T):
			byte1Boolean.append(T)
		elif i is int(F):
			byte1Boolean.append(F)
		else: sys.exit()
	for j in byte2:
		if j is int(T):
			byte2Boolean.append(T)
		elif j is int(F):
			byte2Boolean.append(F)
		else: sys.exit()

	byte1Boolean = byte1Boolean[::-1] ; byte2Boolean = byte2Boolean[::-1] # reverse list's

	while k < MAX_BITS:
		s, c = full_Adder(byte1Boolean[k], byte2Boolean[k], c)
		if s:
			arr.append(int(T))
		else:
			arr.append(int(F))
		k += 1

	return byte1, byte2, arr[::-1], c

if __name__ == '__main__':
	byte1, byte2, arr, carry = byte_Adder("00111111", "10101010")
	
	print byte1, "-> X"
	print byte2, "-> Y"
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ +"
	print arr, "-> X + Y"
	print "Carry Overflow: ", int(carry)
