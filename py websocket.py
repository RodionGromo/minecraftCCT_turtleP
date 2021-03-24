import asyncio
import websockets
import json

global cnt
cnt = 0;

def parseJSONrecv(msg):
	pJSON = json.loads(msg);
	pJSONkeys = pJSON.keys();
	pJSONRkeys = [];
	for key in pJSONkeys:
		pJSONRkeys.append(key)
	if pJSONRkeys[0] == 'message':
		return 'Undefined command|Welcome message:\n ' + pJSON['message']
	elif pJSONRkeys[0] == 'fuelAmount':
		return 'Fuel left: ' + pJSON['fuelAmount']
	elif pJSONRkeys[0] == 'status':
		return 'Returned status: ' + pJSON['status']
	pass

async def basicServer(websocket, path):
	global cnt
	cnt = cnt + 1;
	if(cnt == 1):
		print('Server online! ' + str(cnt))
	msgfc = await websocket.recv()
	print(parseJSONrecv(msgfc));
	while True:
		msg = input('Anyting to client? \n> ')
		if msg == 'exit':
			cnt = 0;
			break
		try:
			info = await websocket.send(msg)
			break
		except:
			print('Total faliure!')
			break
		msg = ''
		print('sent message')

start_server = websockets.serve(basicServer,'localhost',9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
