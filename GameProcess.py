# This class represents a single game process. It is used to keep track of
# running processes, provide save and restore functionality and for garbage
# collection

import os      # used to check for file existence & change directory to SAVE_DIR
import pexpect # for process communication

class GameProcess:
	# Directory for saved games (omit trailing /)
	SAVE_DIR = 'saved_games'

	# Constructor
	def __init__(self, id):
		# change directory if needed
		if not self.SAVE_DIR in os.getcwd():
			os.chdir(self.SAVE_DIR)

		# local variables
		self.id = id
		self.active = True
		
		# if a saved game exists restore it
		if os.path.isfile(str(id)):
			self.proc = pexpect.spawnu('python3 -madventure ' + str(id))
			self.getOutput() # avoid 'GAME RESTORED' message
		else:
			self.proc = pexpect.spawnu('python3 -madventure')
	
	# Destructor
	def __del__(self):
		self.save()
		self.quit()

	# Quit the current game without saving
	def quit(self):
		self.proc.kill(0)
	
	# Save the game
	def save(self):
		self.proc.sendline('save ' + str(self.id))
		self.proc.expect('>')
		self.proc.before
	
	# Restart the game
	def restart(self):
		if os.path.isfile(str(self.id)):
			os.remove(str(self.id))
		
		self.proc.kill(0)
		self.proc = pexpect.spawnu('python3 -madventure')
		
	# Execute a command inside the game (sanitizes its input)
	def execCmd(self, cmd):
		# tell the GC this process is active
		self.active = True
		
		# prevent the user from saving the game (done automatically)
		if 'save' in cmd.lower():
			return "%s\nYOUR GAME IS SAVED AUTOMATICALLY. THERE'S NO " \
				"NEED TO DO THIS MANUALLY." % cmd
		if 'pause' in cmd.lower() or 'suspe' in cmd.lower():
			return "%s\nTO PAUSE THE GAME JUST IGNORE ME. AS LONG AS " \
				"YOU KEEP THIS CHAT OPEN YOUR PROGRES IS NOT LOST." % cmd
		
		# prevent user from quitting
		if 'quit' in cmd.lower():
			return "%s\nTO QUIT JUST REMOVE THIS CHAT." % cmd
		if 'score' in cmd.lower():
			return "%s\nWHAT?" % cmd

		self.proc.sendline(cmd)
		
		return self.getOutput()
	
	# Get output without sending command (avoid locking if unneeded)
	def getOutput(self):
		retStr = ""
		
		try:
			while True:
				self.proc.expect('>', timeout=1)
				retStr = retStr + self.proc.before
		except pexpect.TIMEOUT:
			return retStr
	
	# Read the content of 'active' variable
	def isActive(self):
		return self.active
	
	# Mark the process as inactive
	def markInactive(self):
		self.active = False