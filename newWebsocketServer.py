import asyncio
import websockets
import json
from random import randint
commandBuffer = ""
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

async def echo(websocket):
	global CMDs,Robots
	ID = None
	async for message in websocket:
		ID = None
		try:
			lastJSON = json.loads(message)
			try:
				if(lastJSON['id'] != None):
					ID = lastJSON['id']
			except KeyError:
				print("new bot or comander!")
			if(lastJSON["message"] == "socketInfo"):
				print("new log!")
				if(lastJSON["who"] == 'robot'):
					print("a robot!")
					randID = randint(1,100)
					Robots.append({"id":randID,"socket":websocket})
					await websocket.send(f"os.setComputerLabel('{randID}')")
				elif(lastJSON["who"] == "comander"):
					print("a comander!")
					CMDs.append(websocket)
					await websocket.send(json.dumps({"message":"logDone"}))
			elif(lastJSON["message"] == "err"):
				print("something went wrong when sending last message")
			elif(lastJSON["message"] == "returnBool"):
				if(lastJSON["val"] == True):
					print(f"Success from bot {lastJSON['id']}!")
				else:
					print(f"Failure from bot {lastJSON['id']}!")
			elif(lastJSON["message"] == "returnValue"):
				print(f"Values coming from bot {lastJSON['id']}:")
				print(lastJSON["val"])
			elif(lastJSON["message"] == "newCommand"):
				await sendCommandTo(lastJSON["toID"],lastJSON["command"])
			else:
				print("new unknown message!!\n" + message)
		except websockets.exceptions.ConnectionClosedError as e:
			print("connection closed with err (default)")
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