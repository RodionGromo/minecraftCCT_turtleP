json = require "json"
print("opening websocket")
ws = http.websocket("ws://localhost:9000")
if(os.getComputerLabel() ~= nil ) then
	ws.send(json.encode({message="socketInfo",who="robot",id=os.getComputerLabel()}))
else
	ws.send(json.encode({message="socketInfo",who="robot"}))
end

while true do
	message = ws.receive()
	print("Got: " .. message)
	funct = load(message)
	status,value,value2 = pcall(funct)
	if(status) then
		if(value2 ~= nil) then
			string1 = json.encode({message="returnInfo",val=value2,id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		elseif(type(value) == "table") then
			string1 = json.encode({message="returnInfo",val=value,id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		elseif(type(value) == "boolean") then
			string1 = json.encode({message="returnBool",val=value,id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		else
			string1 = json.encode({message="returnValue",val=tostring(value),id=os.getComputerLabel(),fuel=turtle.getFuelLevel()})
		end
		print("good command, sending: " .. string1)
		ws.send(string1)
	else
		print("bad command")
		ws.send(json.encode({message="err",id=os.getComputerLabel(),fuel=turtle.getFuelLevel()}))
	end
end
