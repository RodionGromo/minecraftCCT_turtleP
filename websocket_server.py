# http server -> WEBSOCKET server -> turtles
import websockets, json, random, threading, time
import websockets.sync.server as websocket_server

from additionalClasses import Robot, Message, BotMessage


addr = {"host":"localhost", "port": 9000}

bots = []
botData = []
outData = []
inData = []

def getRobotDataFromFile(robotID):
	if(robotID == -1):
		return None
	if(type(robotID) is not str):
		robotID = str(robotID)
	with open("robotData.json", "r") as robotData:
		data = json.loads(robotData.read())
		for robot in data:
			if robot["robotID"] == robotID:
				return robot
		return None

def loadAllRobotFileData():
	global bots
	with open("robotData.json", "r") as robotData:
		data = json.loads(robotData.read())
		for robot in data:
			if(findRobotIndex(robot["robotID"]) is None):
				bots.append(Robot(robot["robotID"], robot["fuel"], robot["pos"], robot["facing"]))

def saveRobotData():
	print("saving data", [i.getRaw() for i in bots])
	with open("robotData.json", "w", encoding="utf-8") as robotData:
		data = json.dumps([i.getSaveInfo() for i in bots])
		robotData.write(data)

def findRobotIndex(robotID: str):
	if(type(robotID) is not str):
		robotID = str(robotID)
	for i in range(len(bots)):
		if(bots[i].id == robotID):
			return i
	return None

def findFBMessageFromId(rid):
	print(f"Finding message for id {rid} ({type(rid)})")
	for i in range(len(inData)):
		msg = inData[i]
		if(str(msg.id) == str(rid)):
			content = msg.content
			del inData[i]
			return content
	return None

def generateID():
	return str(random.randint(10000,100000))

def parseTurtleCommand(robotID):
	global bots
	currentBot = bots[findRobotIndex(robotID)]
	if(currentBot.lastCommand == "turtle.turnRight()"):
		print("turtle rotate right")
		if(currentBot.facing == "-z"):
			currentBot.facing = "+x"
		elif(currentBot.facing == "+z"):
			currentBot.facing = "-x"
		elif(currentBot.facing == "+x"):
			currentBot.facing = "+z"
		elif(currentBot.facing == "-x"):
			currentBot.facing = "-z"

	if(currentBot.lastCommand == "turtle.turnLeft()"):
		print("turtle rotate left")
		if(currentBot.facing == "-z"):
			currentBot.facing = "-x"
		elif(currentBot.facing == "+z"):
			currentBot.facing = "+x"
		elif(currentBot.facing == "-x"):
			currentBot.facing = "+z"
		elif(currentBot.facing == "+x"):
			currentBot.facing = "-z"

	if(currentBot.lastReturn[0] == True):
		if(currentBot.lastCommand == "turtle.forward()"):
			if(currentBot.facing == "+x"):
				currentBot.pos.x += 1
			elif(currentBot.facing == "-x"):
				currentBot.pos.x -= 1
			elif(currentBot.facing == "+z"):
				currentBot.pos.z += 1
			elif(currentBot.facing == "-z"):
				currentBot.pos.z -= 1

		if(currentBot.lastCommand == "turtle.back()"):
			if(currentBot.facing == "+x"):
				currentBot.pos.x -= 1
			elif(currentBot.facing == "-x"):
				currentBot.pos.x += 1
			elif(currentBot.facing == "+z"):
				currentBot.pos.z -= 1
			elif(currentBot.facing == "-z"):
				currentBot.pos.z += 1

		if(currentBot.lastCommand == "turtle.up()"):
			currentBot.pos.y += 1

		if(currentBot.lastCommand == "turtle.down()"):
			currentBot.pos.y -= 1

def one_cycle_ws(ws, message):
	ws.send(message)
	ws.recv()

def handle_new_ws(ws):
	global inData, outData, bots
	# websocket init to decide how to treat it
	currentID = -1
	data = json.loads(ws.recv())
	if(data["message"] != "socketInfo"):
		ws.send(json.dumps({"message": "identificationRequired", "data": "Send json message 'socketInfo' with 'id' -1 if you're a server"}))
		ws.close()
		return
	print(data)
	if("id" in data):
		if(type(data["id"]) is not int):
			currentID = int(data["id"])
		else:
			currentID = data["id"]
	else:
		botID = generateID()
		one_cycle_ws(ws, f'os.setComputerLabel("{botID}")')
		bots.append(Robot(botID))
	if(currentID != -1):
		# bot cycle
		# init robot, read all file data to not delete accidentally
		loadAllRobotFileData()
		# we won't read at all by ourself, just wait for messages to appear, send them and only then read
		while True:
			try:
				for message in outData:
					if(str(message.id) == str(currentID)):
						#send message, remove from outgoing, update bot
						ws.send(message.content)
						print(f"[ROBOT] Send {message.content} to robot {currentID}")
						currentBot = bots[findRobotIndex(currentID)]
						currentBot.lastCommand = message.content
						outData.remove(message)

						# receive message, resolve values, save to bot and send to ingoing
						data = json.loads(ws.recv())
						if(data["message"] == "commandError"):
							print(f"[ROBOT] Robot {currentID} received incorrect command")
							currentBot.fuel = data["fuel"]
							currentBot.lastReturn = [False,"incorrect instruction"]
							inData.append(Message(currentBot.lastReturn, currentID))
							saveRobotData()
						elif(data["message"] == "returnData"):
							print(f"[ROBOT] Robot {currentID} returned data")
							currentBot.fuel = data["fuel"]
							val1 = data["val1"] if "val1" in data else None
							val2 = data["val2"] if "val2" in data else None
							print(f"Values: {val1} | {val2}")
							currentBot.lastReturn = [val1,val2]
							inData.append(Message(currentBot.lastReturn, currentID))
							parseTurtleCommand(currentID)
							saveRobotData()
			except websockets.exceptions.ConnectionClosedError:
				print("Robot websocket died, robot:", currentID)
				return
	else:
		# server cycle
		while True:
			try:
				# try to get incoming data
				data = json.loads(ws.recv())
				command = data["message"]
				if(command == "getBots"):
					print("[HTTP SOCKET] Server requested all bot data")
					msg = json.dumps({"message":"botData", "data":[bot.id for bot in bots]})
					ws.send(msg)

				elif(command == "getBot"):
					print("[HTTP SOCKET] Server requested certain bot data")
					bot_ind = findRobotIndex(data["id"])
					if(bot_ind is not None):
						msg = json.dumps({"message": "botInfo", "data": bots[bot_ind].getRaw()})
					else:
						if(data["id"] == "0"):
							msg = json.dumps({"message": "botInfo", "data": bots[0].getRaw()})
						else:
							msg = json.dumps({"message": "botInfo", "data": None})
					ws.send(msg)

				elif(command == "turtleCommand"):
					print("[HTTP SOCKET] Server send command to bot", data["id"])
					bot_ind = findRobotIndex(data["id"])

					if(bot_ind is not None):
						if("data" in data):
							outData.append(Message(data["data"], data["id"]))
							returnData = findFBMessageFromId(data["id"])
							while returnData is None:
								returnData = findFBMessageFromId(data["id"])
								time.sleep(0.1)
							msg = json.dumps({"message": "turtleCommand", "id": data["id"], "data": returnData})
						else:
							msg = json.dumps({"message": "noData", "id": data["id"], "warning": "No 'data' field provided, add it and try again"})
					else:
						msg = json.dumps({"message": "turtleCommand", "data": None, "warning": f"Bot with id {data['id']} not found"})
					ws.send(msg)
			except websockets.exceptions.ConnectionClosedError:
				print("[HTTP SOCKET] Server closed connection")
				return

		

ws_server = websocket_server.serve(handle_new_ws, addr["host"], addr["port"], compression=None)
serverThread = threading.Thread(target=ws_server.serve_forever, group=None)
serverThread.start()
print("Websocket server started!")
lastArray = []
while True:
	if lastArray != bots:
		print("array update ---------------")
		for robot in bots:
			print("\tBot", robot.id, "- fuel:", robot.fuel)
		print("array end ------------------")
		lastArray = bots.copy()
	
