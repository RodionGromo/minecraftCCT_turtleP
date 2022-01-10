json = require "json"
print("opening websocket")
ws = http.websocket("ws://localhost:9000")
ws.send(json.encode({message="socketInfo",who="robot"}))
while true do
	message = ws.receive()
	print("Got: " .. message)
	funct = load(message)
	status,value,value2 = pcall(funct)
	if(status) then
		if(value2 ~= nil) then
			string1 = json.encode({message="returnInfo",val=value2,id=os.getComputerLabel()})
		elseif(value == nil) then
			string1 = json.encode({message="returnBool",val=status,id=os.getComputerLabel()})
		else
			string1 = json.encode({message="returnValue",val=tostring(value),id=os.getComputerLabel()})
		end
		print("good command, sending: " .. string1)
		ws.send(string1)
	else
		print("bad command")
		ws.send(json.encode({message="err",id=getComputerLabel()}))
	end
end