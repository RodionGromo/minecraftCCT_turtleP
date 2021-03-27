import asyncio
import websockets
import json
from flask import Flask,redirect
httpport = 8000

file = open("./site.html","r",encoding="utf-8")
inFile = file.read()

global commandBuffer
commandBuffer = []

global cnt
cnt = 0;

global turltleParams
turltleParams = {"fuel":0,'test':True}

app = Flask(__name__)

#flask html server routes
@app.route('/')
def mainPage():
	return inFile

@app.route('/command/<command>/')
def commandRun(command):
	global commandBuffer
	commandBuffer.append(command)
	print(commandBuffer)
	return 'true'

@app.route('/yield/<toYield>/')
def yieldVar(toYield):
	global turltleParams
	print("Yield: " + toYield)
	if(toYield == 'fuel'):
		return str(turltleParams["fuel"])
	else:
		return 'false'

@app.route('/put/<intType>/<value>/')
def putVar(intType,value):
	global turltleParams;
	if(intType == 'fuel'):
		turltleParams["fuel"] = int(value);
		return "true"
	else:
		return "false"

@app.route('/getCommands')
def getOneCommandFromBuffer():
	global commandBuffer
	if(len(commandBuffer) > 0):
		return commandBuffer.pop()
	else:
		return 'false'

if __name__ == '__main__':
	print('running html')
	app.run(port=httpport)
