import asyncio
import websockets
import json
from random import randint
commandBuffer = []
CMDs = []
Robots = []


def removeID(aid):
	global Robots,CMDs
	lastTime = None;
	for obj in Robots:
		if(aid == obj["id"]):
			print(f"Removed robot {obj['id']}")
			Robots.remove(obj)
			
	for cid in CMDs:
		if(aid == cid):
			print(f"Removed comander {cid}")
			CMDs.remove(obj)

def findIDreturnSocket(Id):
	global Robots
	for obj in Robots:
		if(Id == obj['id']):
			return obj['socket']

async def sendCommandTo(idr,command):
	global Robots
	socket = findIDreturnSocket(idr)
	await socket.send("return " + command)

def updateFuel(idr,fuel):
	global Robots
	for robot in Robots:
		if(idr == robot['id']):
			robot['fuel'] = fuel;

def isOkID(rid):
	rid = int(rid)
	if(0 < rid < 100):
		return True
	else:
		return False

def getRobots():
	global Robots
	newArr = []
	if(len(Robots) > 0):
		for robot in Robots:
			newArr.append({"id":robot['id'],"fuel":robot['fuel']})
		return newArr
	else:
		return {"message":"err"}

async def sendToComander(sender,value,typeofInfo):
	global CMDs
	for comander in CMDs:
		if(str(sender) == str(comander['id'])):
			print(f"Sent a message to {sender} with value: {value}")
			await comander['ws'].send(json.dumps({"message":"returnValue","val":value,"infoType":typeofInfo}))

async def returnToSender(robotID,value,typeofInfo):
	global commandBuffer
	for request in commandBuffer:
		if(str(robotID) == str(request['toBot'])):
			await sendToComander(request['sender'],value,typeofInfo)
			commandBuffer.remove(request)
	print(commandBuffer)

async def echo(websocket):
	global CMDs,Robots,commandBuffer
	ID = None
	async for message in websocket:
		ID = None
		try:
			print(f"New message: {message}")
			lastJSON = json.loads(message)
			try:
				if(lastJSON['id'] != None):
					ID = lastJSON['id']
			except KeyError:
				if(lastJSON["message"] == "socketInfo"):
					print("new bot or comander!")
			if(lastJSON["message"] == "socketInfo"):
				print("new log!")
				if(lastJSON["who"] == 'robot'):
					randID = randint(1,100)
					if(isOkID(lastJSON['id']) and lastJSON['id'] != None):
						randID = lastJSON['id']
						print("bot got an id, putting it in")
					else:
						print("giving a bot id")
					print("a robot!")
					Robots.append({"id":randID,"socket":websocket,"fuel":None})
					await websocket.send(f"os.setComputerLabel('{randID}')")
				elif(lastJSON["who"] == "comander"):
					print("a comander!")
					randID = randint(100,200)
					CMDs.append({"ws":websocket,"id":randID})
					await websocket.send(json.dumps({"message":"logDone","uniqueID":randID}))
			elif(lastJSON["message"] == "err"):
				await returnToSender(lastJSON["id"],"none","crit")
			elif(lastJSON["message"] == "returnBool"):
				updateFuel(lastJSON["id"],lastJSON['fuel'])
				await returnToSender(lastJSON["id"],lastJSON["val"],"state")
				# if(lastJSON["val"] == True):
				# 	print(f"Success from bot {lastJSON['id']}!")
				# else:
				# 	print(f"Failure from bot {lastJSON['id']}!")
			elif(lastJSON["message"] == "returnValue"):
				updateFuel(lastJSON["id"],lastJSON['fuel'])
				await returnToSender(lastJSON["id"],lastJSON["val"],'state')
				# print(f"Values coming from bot {lastJSON['id']}:")
				# print(lastJSON["val"])
			elif(lastJSON['message'] == 'returnInfo'):
				updateFuel(lastJSON["id"],lastJSON['fuel'])
				if(type(lastJSON["val"]) != str):
					await returnToSender(lastJSON["id"],lastJSON["val"],"block")
				else:
					await returnToSender(lastJSON["id"],lastJSON["val"],"stringInfo")
			elif(lastJSON["message"] == "newCommand"):
				commandBuffer.append({"toBot":lastJSON["toID"],"sender":lastJSON["comanderID"]})
				await sendCommandTo(lastJSON["toID"],lastJSON["command"])
			elif(lastJSON['message'] == "getRobots"):
				await websocket.send(json.dumps({"message":"returnBots","bots":getRobots()}))
			else:
				print("new unknown message!!\n" + message)
		except (Exception,websockets.exceptions.ConnectionClosedError) as e:
			print(e)
			print("connection closed")
			if(ID != None):
				removeID(ID)

async def main():
	global Robots
	async with websockets.serve(echo, "localhost",9000,compression=None):
		if(len(Robots) > 0):
			for obj in Robots:
				await obj["socket"].ping()
		await asyncio.Future()  # run forever

asyncio.run(main())
