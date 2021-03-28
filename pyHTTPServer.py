import os
import json
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


file = open("./site.html","r",encoding="utf-8")
inFile = file.read()

global commandBuffer
commandBuffer = []

global cnt
cnt = 0;

global turltleParams
turltleParams = {"fuel":0}

app = Flask(__name__)

def getNoiceResponse(cobject):
	response = make_response(cobject)
	response.headers["Access-Control-Allow-Origin"] = '*'
	return response

def getFileByName(name):
	global textures
	localTexture = textures
	print(localTexture)

#flask html server routes
@app.route('/')
def mainPage():
	return getNoiceResponse(inFile)

@app.route('/command/<command>/')
def commandRun(command):
	global commandBuffer
	commandBuffer.append(command)
	print(commandBuffer)
	return getNoiceResponse('true')

@app.route('/yield/<toYield>/')
def yieldVar(toYield):
	global turltleParams
	print("Yield: " + toYield)
	if(toYield == 'fuel'):
		return getNoiceResponse(str(turltleParams["fuel"]))
	else:
		return getNoiceResponse('false')

@app.route('/put/<intType>/<value>/')
def putVar(intType,value):
	global turltleParams;
	if(intType == 'fuel'):
		turltleParams["fuel"] = int(value);
		return getNoiceResponse("true")
	else:
		return getNoiceResponse("false")

@app.route('/getCommands')
def getOneCommandFromBuffer():
	global commandBuffer
	if(len(commandBuffer) > 0):
		return getNoiceResponse(commandBuffer.pop())
	else:
		return getNoiceResponse('false')

@app.route('/returnRsp/<RspObject>')
def parseResponse(RspObject):
	print(RspObject)
	return getNoiceResponse('noice')

@app.route('/getTexture/<name>')
def getTexture(name):
	for file in textures:
		if(name == file['name']):
			return getNoiceResponse(send_file('./blocks/{0}'.format(file['filename'])))

@app.route('/getTexture')
def getTextureNames():
	return getNoiceResponse(str(textures));


if __name__ == '__main__':
	print('running html')
	app.run(port=httpport,host='25.84.31.18')
