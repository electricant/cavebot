# This class holds a list of the running processes. It is responsible for
# creating and fetching them as well as destroying the unused ones
import time
import threading

from GameProcess import GameProcess

class ProcessList:
	# Maximum allowed number of children
	MAX_CHILDREN = 100;
	# Minimum number of children. If there is this number of children the GC
	# is not started
	MIN_CHILDREN = 10;
	# Time interval between two consequent GC runs. 
	# NOTE: the GC is run also whenever the number of children reaches its
	# maximum value
	GC_INTERVAL_SEC = 30;

	# Constructor
	def __init__(self):
		# local variables
		self.pDict = dict() # dictionary storing the running processes
		
		# start thread for garbage collection
		self.GCThreadStop = False
		self.GCThread = threading.Thread(target=self.GCThreadFunction)
		self.GCThread.start()
	
	# Destructor
	def __del__(self):
		self.stopGC()

	# Manually stop the Garbage Collector thread
	def stopGC(self):
		if not self.GCThreadStop:
			print("Stopping GC thread...")
			self.GCThreadStop = True
			self.GCThread.join()

	# Get a process. It will create a new one if it does not exist
	def getGame(self, id):
		if not id in self.pDict:
			if len(self.pDict) == self.MAX_CHILDREN:
				self.runGC()
				if len(self.pDict) == self.MAX_CHILDREN:
					return None
			# if we get here a new process can be spawned
			self.pDict[id] = GameProcess(id)
		
		return self.pDict[id]
	
	# Helper function that destroys long running processes
	def runGC(self):
		newDict = dict()
		startSize = len(self.pDict)

		for (proc_id, proc) in self.pDict.items():
			if proc.isActive():
				proc.markInactive()
				newDict[proc_id] = proc

		self.pDict = newDict
		print("Stopped: %u" % (startSize - len(newDict)))
	# Function that returns the dictionary with all the precesses
	def getAll(self):
		return self.pDict
	
	# Function used for the GC thread
	def GCThreadFunction(self):
		while not self.GCThreadStop:
			time.sleep(self.GC_INTERVAL_SEC)
			if len(self.pDict) > self.MIN_CHILDREN:
				self.runGC()
