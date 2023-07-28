import pygetwindow as gw
import subprocess
import keyboard
import time
import os

os.system("cls")

window_height = 600
window_width = 800

is_restarted = False
current = 0
stime = 0
mtime = 0
htime = 0

def fix_window():
	window = gw.getActiveWindow()

	window.moveTo(0, 0)
	window.restore()
	window.resizeTo(window_width, window_height)

fix_window()

while True:
	if is_restarted == True:
		fix_window()
		print("")
		print("")
		print("")
		print("")
		print("	>   \033[36mRestarting :)\033[39m")
		time.sleep(3)
		fix_window()
		os.system("cls")
	print("")
	print("	      _____________________________________________________________")
	print("	     |                                                             |")
	print("	     |    Maangas na Anti-AFK para sa roblox :)                    |")
	print("	     |                                                             |")
	print("	     |    The purpose of this code is to prevent Roblox from       |")
	print("	     |    kicking the player for being AFK for 20 minutes. long    |")
	print("	     |                                                             |")
	print("	     |    Created by: Carl Matchu                                  |")
	print("	     |                                                             |")
	print("	      ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
	print("\033[14;1H	>   Checking for Roblox       ")

	def process_exists(process_name):
		progs = str(subprocess.check_output('tasklist'))
		if process_name in progs:
			return True
		else:
			return False
		
	while process_exists("RobloxPlayerBeta.exe") == False:
		fix_window()

		time.sleep(0.2)
		print("\033[14;1H	>   Checking for Roblox |     ")
		print("\033[15;1H	>   \033[91m(Not found)\033[39m")
		time.sleep(0.2)
		print("\033[14;1H	>   Checking for Roblox /     ")
		print("\033[15;1H	>   \033[91m(Not found)\033[39m")
		time.sleep(0.2)
		print("\033[14;1H	>   Checking for Roblox —     ")
		print("\033[15;1H	>   \033[91m(Not found)\033[39m")
		time.sleep(0.2)
		print("\033[14;1H	>   Checking for Roblox \     ")
		print("\033[15;1H	>   \033[91m(Not found)\033[39m")

	print("\033[14;1H	>   Checkpoint success!        ")
	print("\033[15;1H	>   \033[92m(Roblox found)\033[39m")
	print("")
	print("	>   \033[94mNOTE:\033[39m")
	print("		1. This Anti-AFK works on every game and undetectable by any system.")
	print("		2. Anti-AFK works only when Roblox is on the screen. It won't work if\n		   you Alt Tab or switch to another window.")
	print("		3. Do not open the chatbox or anything that you could type letters on.")
	print("")
	if is_restarted == True:
		print("	>   App restarted...")
		if mtime == 0 and htime == 0:
			print(f"	>   \033[36mYou've been AFK for:\033[39m \033[93m{stime}s\033[39m")
		elif mtime > 0 and htime == 0:
			print(f"	>   \033[36mYou've been AFK for:\033[39m \033[93m{mtime}m {stime}s\033[39m")
		elif mtime > 0 and htime > 0:
			print(f"	>   \033[36mYou've been AFK for:\033[39m \033[93m{htime}h {mtime}m {stime}s\033[39m")

		is_restarted = False
		current = 0
		stime = 0
		mtime = 0
		htime = 0

	print("")
	print("	>   \033[33mHow to use?\033[39m")
	print("		1. Play any game")
	print("		2. Press 'T' to activate")
	print("		3. Stop playing roblox.")
	print("")

	while True:
		window = gw.getActiveWindow()
		
		if window.height != window_height or window.width != window_width or window.left != 0 or window.top != 0:
			fix_window()

		if keyboard.read_key() == "t":
			print("	>   \033[95mAnti-AFK is now activated.\033[39m")
			print("	>   Hold 'T' to deactivate")
			print("")
			print("")
			break

	time.sleep(1)

	while True:
		fix_window()

		if keyboard.is_pressed("t") or process_exists("RobloxPlayerBeta.exe") == False:
			os.system("cls")
			is_restarted = True
			break

		if stime in [0, 10, 20, 30, 40, 50]:
			if current == 0:
				keyboard.press("a")
				current += 1
			elif current == 1:
				keyboard.press("s")
				current += 1
			elif current == 2:
				keyboard.press("d")
				current += 1
			elif current == 3:
				keyboard.press("w")
				current = 0

		time.sleep(1)
		keyboard.release("a")
		keyboard.release("s")
		keyboard.release("d")
		keyboard.release("w")
		keyboard.release("space")

		stime += 1
		if stime == 30:
			keyboard.press("space")

		if stime >= 60:
			stime = 0
			mtime += 1
			if mtime >= 60:
				mtime = 0
				htime += 1
				
		if mtime == 0 and htime == 0:
			print(f"	>   \033[36mYou've started Anti-AFK for:\033[39m \033[93m{stime}s\033[39m", end="\r")
		elif mtime > 0 and htime == 0:
			print(f"	>   \033[36mYou've started Anti-AFK for:\033[39m \033[93m{mtime}m {stime}s\033[39m", end="\r")
		elif mtime > 0 and htime > 0:
			print(f"	>   \033[36mYou've started Anti-AFK for:\033[39m \033[93m{htime}h {mtime}m {stime}s\033[39m", end="\r")