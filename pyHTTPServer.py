import os
import json
import time
from random import randint
from flask import Flask,redirect,send_file,make_response
httpport = 8000

def readAllTextures():
	files = os.listdir('./blocks')
	textures = [];
	for filename in files:
		buf1 = {"name":filename.split('.')[0],'filename':filename}
		textures.append(buf1)
	return textures

textures = readAllTextures()
turtleFileLoc = '/turtles.json'

file = open("./site.html","r",encoding="utf-8")
inFile = file.read()
JSON_ok = '{"type":"message","message":"Successfull"}'
JSON_error = '{"type":"error","message":"Error"}'
global commandBuffer
commandBuffer = []

global cnt
cnt = 0;

arr_en = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

global turtles
# turtle['id'] = {"id":id,fuel:0,"pos":[0,0,0]}
turtles = [];

app = Flask(__name__)

def getNewId():
	newId = ''
	for i in range(0,4):
		newId = newId + arr_en[randint(0,len(arr_en) - 1)]
	return newId

def getJsonBlocks():
	return 'false'

def gNR(cobject):
	response = make_response(cobject)
	response.headers["Access-Control-Allow-Origin"] = '*'
	return response

def getFileByName(name):
	global textures
	localTexture = textures
	print(localTexture)

def getTurtles():
	global turtles
	string = ''
	string = json.dumps(turtles)
	return string

def getVfTA(turtleId,var):
	global turtles
	for turtle in turtles:
		if(turtleId == turtle['id']):
			return turtle[var]

def setVfTA(turtleId,var,value):
	global turtles
	for turtle in turtles:
		if(turtleId == turtle['id']):
			if(var == 'fuel'):
				value = int(value)
			try:
				turtle[var] = value
				return True
			except Exception as e:
				print(e)
				return False

def saveTurtle():
	global turtles
	turtleFile = open(turtleFileLoc,'w')
	turtleFile.write(str(json.dumps(turtles)))
	turtleFile.close()

def getRandomTurtle():
	return {"id":getNewId(),'fuel':randint(0,1024),'pos':[randint(0,1024),randint(0,1024),randint(0,1024)]}

def getCommandById(Turtleid):
	global commandBuffer
	for command in commandBuffer:
		if(command['id'] == Turtleid):
			return commandBuffer.pop(commandBuffer.index(command))

#flask html server routes
@app.route('/')
def mainPage():
	return gNR(inFile)

@app.route('/command/<command>/<turtleId>')
def commandRun(command,turtleId):
	global commandBuffer
	commandBuffer.append({"id":turtleId,"value":command})
	print(commandBuffer)
	return gNR(JSON_ok)

@app.route('/yield/<toYield>/<turtleId>')
def yieldVar(toYield,turtleId):
	print("Yield: " + toYield)
	if(toYield == 'fuel'):
		return gNR(json.dumps({"value":getVfTA(turtleId,toYield),"type":toYield,"turtleId":turtleId}))
	else:
		return gNR('{"type":"error","message":"No such turtle exists!"}')
	return gNR('{"type":"error","message":"No such turtle exists!"}')

@app.route('/put/<intType>/<value>/<turtleId>')
def putVar(intType,value,turtleId):
	response = setVfTA(turtleId,intType,value)
	saveTurtle();
	if(response == True):
		return gNR(JSON_ok)
	else:
		return gNR(JSON_error)

@app.route('/getCommands/<turltleId>')
def getOneCommandFromBuffer(turltleId):
	global commandBuffer
	if(len(commandBuffer) > 0):
		return gNR(getCommandById(turltleId))
	else:
		return gNR(JSON_error)

@app.route('/returnRsp/<RspObject>/<turltleId>')
def parseResponse(RspObject):
	print(RspObject)
	return gNR(JSON_ok)

@app.route('/getTexture/<name>')
def getTexture(name):
	for file in textures:
		if(name == file['name']):
			return gNR(send_file('./blocks/{0}'.format(file['filename'])))

@app.route('/getNewId/<timedId>')
def createNewId(timedId):
	return gNR(getNewId())

@app.route('/getAllTurtles')
def getAllTurtles():
	return gNR('{"type":"allTurtles","value":' + getTurtles() + '}')

@app.route('/getTexture')
def getTextureNames():
	return gNR(str(textures));

@app.route('/getBlocksJSON')
def getJsonBlock():
	return gNR(JSON_error)


@app.route('/softShutdown')
def softOff():
	return gNR(JSON_ok)

@app.route('/register/<turtleId>/<x>/<y>/<z>/<direction>')
def regNewBot(turtleId,x,y,z,direction):
	global turtles
	for turtle in turtles:
		if(turtle['id'] == turtleId):
			return 'error'
	turtles.append({"id":turtleId,"pos":[x,y,z],"dir":direction,"fuel":None,'lastActive':time.time() * 1000})
	return 'ok'

@app.route('/spamTurtle/<count>')
def addTurtles(count):
	global turtles
	count = int(count)
	for i in range(0,count):
		turtles.append(getRandomTurtle())
	return gNR(JSON_ok)

if __name__ == '__main__':
	print('running html')
	app.run(port=httpport,host='25.84.31.18')
