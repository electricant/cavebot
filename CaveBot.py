import telegram.botapi.botbuilder as botbuilder
import pexpect
import signal
import sys

from GameProcess import GameProcess
from ProcessList import ProcessList
#
# Global variables
#
global games

#
# Helper functions
#

# Display an help text
def help_text(update):
	return "@cave_bot - Play Colossal Cave Adventure!\n" \
		"This is the list of commands:\n\n" \
		"/restart - Starts a new game\n" \
		"/cave - Tell the bot what to do\n" \
		"/help - Display this help text.\n\n" \
		"Created by: The Electric Ant\n" \
		"If you like this game please consider making a donation " \
		"https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XSKMSYEX77FZ4"

# Cleanup and save game before quitting
def exitGracefully(signal, frame):
	global games
	
	for proc in games.getAll().values():
		proc.save()
		proc.quit()
		
	games.stopGC()
	
	print("GOODBYE.")
	sys.exit(0)

# Start a new game
def start(update):
	global games
	
	game = games.getGame(update.chat.id)
	if game == None:
		return "Sorry, the server is busy. Try again later."
	
	return game.getOutput()

# process user input
def process_input(update):
	global games
	
	game = games.getGame(update.chat.id)
	if game == None:
		return "Sorry, the server is busy. Try again later."
	
	if len(update.text) >= 7:
		return game.execCmd(update.text[6:])
	else:
		return game.getOutput()

# Start a new game
def restart(update):
	game = games.getGame(update.chat.id)
	
	game.restart()
	return game.getOutput()

# Log received messages
def logger(update):
	print("%i > %s" % (update.chat.id, update.text))
	
#
# MAIN:
#
if __name__ == "__main__":
	# create games list
	global games
	games = ProcessList()
	# intercept SIGINT (Ctrl+C)
	signal.signal(signal.SIGINT, exitGracefully)
	# create bot
	bot = botbuilder.BotBuilder(apikey_file="apikey.txt")
	# bot actions
	bot.do_when(lambda update: (True), logger, botbuilder.DO_NOT_CONSUME)
	bot.send_message_when("start", start)
	bot.send_message_when("cave", process_input)
	bot.send_message_when("help", help_text)
	bot.send_message_when("restart", restart)
	# create bot and launch it
	bot.build().start()
