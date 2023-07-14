import json

class Vector3:
	def __init__(self, x=None, y=None, z=None, posArray=None):
		if(posArray is not None):
			self.x = posArray[0]
			self.y = posArray[1]
			self.z = posArray[2]
		else:
			self.x = x
			self.y = y
			self.z = z

	def __repr__(self):
		return [self.x, self.y, self.z]

	def raw(self):
		return self.__repr__()

class Robot:
	def __init__(self, robotID, fuel=0, pos=[0,0,0], facing="+x"):
		self.id = robotID;
		self.fuel = fuel

		self.lastReturn = [None, None]
		self.lastCommand = ""
		self.pos = Vector3(posArray=pos)
		self.facing = facing

	def getRaw(self):
		return {"robotID": self.id, "fuel": self.fuel, "lastData": self.lastReturn, "lastCommand": self.lastCommand, "pos": self.pos.raw(), "facing": self.facing}

	def getSaveInfo(self):
		return {"robotID": self.id, "fuel": self.fuel, "pos": self.pos.raw(), "facing": self.facing}

class Message:
	def __init__(self, message, forID):
		self.content = message
		self.id = forID

	def __repr__(self):
		return f"[Message '{self.content}' for id {self.id}]"

class BotMessage:
	def __init__(self, val1, val2, botID):
		self.content = [val1, val2]
		self.id = botID

class HTTPMessage:
	def __init__(self, message, userID, in_data=None):
		self.content = message
		self.userID = userID
		self.in_data = in_data

	def getJSON(self):
		if(self.in_data is not None):
			return json.dumps({"message":self.content, "id": self.userID, "data":self.in_data})
		else:
			return json.dumps({"message":self.content, "id": self.userID})

	def __repr__(self):
		return f"[Message: {self.content}, ID: {self.userID}]"