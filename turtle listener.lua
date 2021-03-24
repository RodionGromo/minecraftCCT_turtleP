print("Don't forget F3 + P!")
local myURL = "ws://localhost:9000"
local ws,err = nil
local sendString = '{"message":"Ready!"}'

function getFuelSlot()
	return 64 - turtle.getItemSpace(turtle.getSelectedSlot())
end

function parseMsg(msg)
	if msg == 'fw' then
		sendString = '{"status":"' .. tostring(turtle.forward()) .. '"}'
		return true
	elseif msg == 'bk' then
		sendString = '{"status":"' .. tostring(turtle.back()) .. '"}'
		return true
	elseif msg == 'rl' then
		sendString = '{"status":"' .. tostring(turtle.turnLeft()) .. '"}'
		return true
	elseif msg == 'rr' then
		sendString = '{"status":"' .. tostring(turtle.turnRight()) .. '"}'
		return true
	elseif msg == 'fuel' then
		sendString = '{"fuelAmount":"' .. tostring(turtle.getFuelLevel()) .. '"}'
		return true
	elseif msg == 'refuel' then
		sendString = '{"status":"' .. tostring(turtle.refuel(getFuelSlot())) .. '"}'
	else
		return false
	end
end

function connect()
	ws, err = http.websocket(myURL)
	if ws then
		ws.send(sendString)
		sendString = '{"status":"Unknown"}'
		msg = ws.receive()
		response = parseMsg(msg)
		if (response ~= true) then
			print('> ' .. msg)
		end
		sleep(0.25)
		connect()
	else
		sleep(0.25)
		connect()
	end
end

connect()