# HTTP server -> websocket server -> turtles
import flask, json, threading, websockets, time
import websockets.sync.client as ws_client
from additionalClasses import HTTPMessage
from flask import request

ws_addr = {"host":"localhost", "port": 9000}

app = flask.Flask(__name__)
server = ws_client.connect(f"ws://{ws_addr['host']}:{ws_addr['port']}")

init_message = json.dumps({"message":"socketInfo","who":"server","id":-1})
server.send(init_message)

# to_server - send to socket server
# next_assigned - next received message from server will have this id
# from_server - send to http clients
to_server = []
next_assigned = None
from_server = []

def server_talk():
	global to_server, from_server, next_assigned
	while True:
		try:
			data = server.recv(timeout=1)
			decodedData = json.loads(data)
			if(decodedData["message"] == "Welcome!"):
				continue
			#print("[Socket Decoded] >>",decodedData)
			from_server.append(HTTPMessage(decodedData, next_assigned))
			print("[Socket] >>",data)
			#print("Data stored:",from_server)
			next_assigned = None
			#print(from_server)
		except TimeoutError:
			if(len(to_server) > 0):
				message = to_server[0].getJSON()
				next_assigned = to_server[0].userID
				del to_server[0]
				server.send(message)
				print("[Socket] <<", message, " | awaiting:", len(to_server))
		except websockets.exceptions.ConnectionClosedError:
			print("Socket server closed")
			return

def getMesssageForID(mID):
	for i in range(len(from_server)):
		if from_server[i].userID == mID:
			data = from_server[i]
			del from_server[i]
			return data
	return False

def gen_response(data):
	res = flask.make_response(data)
	res.headers["Access-Control-Allow-Origin"] = "*"
	return res

def get_data():
	return json.loads(request.data.decode("utf-8"))

@app.route("/home")
def http_main():
	return gen_response("ok")

@app.route("/parseCommand", methods=["GET", "POST"])
def http_parseCommand():
	print("\n[HTTP] >> new data",request.data.decode("utf-8"))
	try:
		print(request.form.to_dict())
	except Exception:
		print("nop")
	http_data = get_data()
	#print(f"[HTTP] >> new command {http_data}")
	if("data" in http_data):
		to_server.append(HTTPMessage(http_data["command"], http_data["id"], http_data["data"]))
	else:
		to_server.append(HTTPMessage(http_data["command"], http_data["id"]))
	data = getMesssageForID(http_data["id"])
	while not data:
		data = getMesssageForID(http_data["id"])
		time.sleep(0.01)
	print(f"[HTTP] << {http_data['command']} sent back, data:",data)
	return gen_response(json.dumps(data.content))

@app.route("/parseCommandForm", methods=["POST", "GET"])
def http_parseCommandForm():
	print("\n[HTTP] >> new data",request.form.to_dict())
	http_data = request.form.to_dict()
	if("data" in http_data):
		to_server.append(HTTPMessage(http_data["command"], http_data["id"], http_data["data"]))
	else:
		to_server.append(HTTPMessage(http_data["command"], http_data["id"]))
	data = getMesssageForID(http_data["id"])
	while not data:
		data = getMesssageForID(http_data["id"])
		time.sleep(0.01)
	print(f"[HTTP] << {http_data['command']} sent back, data:",data)
	return gen_response(json.dumps(data.content))

server_thread = threading.Thread(target=server_talk)
server_thread.start()
app.run(host="10.8.0.3",port=7890)