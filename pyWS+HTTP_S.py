import asyncio
import websockets
import json
from flask import Flask,redirect
from flask_socketio import SocketIO
httpport = 8000
wsport = 9000

file = open("./vadim.html","r",encoding="utf-8")
inFile = file.read()

global commandBuffer
commandBuffer = []

global cnt
cnt = 0;

global turltleParams
turltleParams = {"fuel":0}

app = Flask(__name__)
socketio = SocketIO(app)

#flask html server routes
@app.route('/')
def mainPage():
	return inFile

@app.route('/command/<command>/')
def commandRun(command):
	global commandBuffer
	commandBuffer.append(command)
	return 'buffer+'

@app.route('/yield/<toYield>/')
def yieldVar(toYield):
	global turltleParams

	if(toYield == 'fuel'):
		return str(turltleParams["fuel"])
	else:
		return 'unknown command'

#flask ws routes
@socketio.on('connect')
def connected():
	print('somebody connected');

def parseJSONrecv(msg):
	try:
		pJSON = json.loads(msg);
		pJSONkeys = pJSON.keys();
		pJSONRkeys = [];
	except:
		return msg

	for key in pJSONkeys:
		pJSONRkeys.append(key)
	if pJSONRkeys[0] == 'message':
		return 'Undefined command|Welcome message:\n ' + pJSON['message']
	elif pJSONRkeys[0] == 'fuelAmount':
		turltleParams["fuel"] = int(pJSON['fuelAmount'])
		return 'Fuel left: ' + pJSON['fuelAmount']
	elif pJSONRkeys[0] == 'status':
		return 'Returned status: ' + pJSON['status']
	else:
		return pJSON
	pass


# async def basicServer(websocket, path):
# 	global cnt
# 	cnt = cnt + 1;
# 	if(cnt == 1):
# 		print('Server online! ' + str(cnt))
# 	msgfc = await websocket.recv()
# 	print(parseJSONrecv(msgfc));
# 	while True:
# 		while len(commandBuffer) > 0:
# 			msg = commandBuffer.pop(0)
# 			if msg == 'restartSocket':
# 				cnt = 0;
# 				break;
# 			try:
# 				info = await websocket.send(msg)
# 				break;
# 			except:
# 				print("Total faliure!")
# 				break;



# start_server = websockets.serve(basicServer,'localhost',9000)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
	print('running html')
	app.run(port=httpport)
	print('running websocket')
	socketio.run(app,port=wsport)