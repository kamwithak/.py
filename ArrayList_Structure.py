# ArrayList Data Structure (OOP)
# Python3
# Developed by Kamran Choudhry

class ArrayList:
	def __init__(self, arr):
		self.arr = arr

	# print array at any given instant
	def printArray(self):
		print('array -> ' + str(self.arr))

	# delete all the elements in the array
	def clearArray(self):
		del self.arr[:]

	# is the array empty or not?
	def isArrayEmpty(self):
		if self.arr:
			print('array is populated')
		else:
			print('array is empty')

	# return length of input array
	def getSize(self):
		return len(self.arr)

	# append to the end of the array
	def appendToArray(self, e):
		self.arr.append(e)

	# get array value at index i
	def getAtIndex(self, i):
		try:
			return self.arr[i]
		except IndexError:
			raise Exception("index out of bounds")

	# array[i] <- e // copy over previous value
	def setAtIndex(self, i, e):
		try:
			self.arr[i] = e
		except IndexError:
			raise Exception("index out of bounds")

	# array[i] <- e where the values at indicies [i,size(array)-1] are shifted to the next index
	def addAtIndex(self, i, e):
		try:
			self.arr.insert(i, e)
		except IndexError:
			raise Exception("index out of bounds")
			
	# delete element at a particular location // readjust indicies
	def removeAtIndex(self, i):
		try:
			del self.arr[i]
		except IndexError:
			raise Exception("index out of bounds")


if __name__ == '__main__':

	arr = ArrayList(['a','b','c','d','e','f','g','h','i','j','k'])
	arr.printArray()
	arr.isArrayEmpty()
	print('size of array is ' + str(arr.getSize()))

	#print(arr.getAtIndex(1))

	arr.addAtIndex(0, 'abc')
	arr.appendToArray('kam')
	arr.printArray()

	arr.clearArray()
	
	arr.isArrayEmpty()
	print('size of array is ' + str(arr.getSize()))
	arr.printArray()






