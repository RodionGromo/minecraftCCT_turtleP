json = require "json"
print("opening websocket")
ws, status = http.websocket("ws://localhost:9000")

if(os.getComputerLabel() ~= nil) then
	ws.send(json.encode({message="socketInfo",who="robot",id=os.getComputerLabel()}))
else
	ws.send(json.encode({message="socketInfo",who="robot"}))
end

while true do
	recv_data = ws.receive()
	if(recv_data == nil) then
		print("websocket was closed or timeout")
		break
	else
		print("Got: " .. recv_data)
		funct = load("return ".. recv_data)
		status,value,value2 = pcall(funct)
		if(status) then
			message = json.encode({message="returnData",val1=value,val2=value2,id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		else
			message = json.encode({message="commandError",id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		end
		ws.send(message)
	end
end
