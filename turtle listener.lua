print("Don't forget F3 + P!");
local myURL = "ws://localhost:9000";
local ws,err = nil;
local sendString = '{"message":"Ready!"}';
local st1 = '{"status":"';
local st2 = '"}'
local statusNone = '{"status":"None"}'

function dropAll()
	i = 1
	successful = 0
	turtle.select(i);
	while i < 17 do
		turtle.select(i)
		if(turtle.getItemSpace(i) ~= 64) then
			turtle.drop()
			successful = successful + 1
		end
		i = i + 1
	end
	turtle.select(1);
	if(successful > 1) then
		return "true"
	else
		return  "false"
	end
end

function fuelCost(itemName)
	if(itemName == "minecraft:coal" or itemName == "minecraft:charcoal") then 
		return 80
	elseif (itemName == "minecraft:coal_block" or itemName == "minecraft:charcoal_block") then
		return 800
	end
	return 0
end

function autoRefuel(arg)
	slot = 1
	refueled = 0 -- 1 coal is 80 points, 1 coal block is 800 points
	arg = tonumber(arg)
	while slot < 17 do
		if (arg ~= nil and refueled < arg) then
			turtle.select(slot)
			tbl = turtle.getItemDetail(slot)
			if(tbl ~= nil) then
				if(tbl.name == "minecraft:coal" or tbl.name == "minecraft:charcoal" or tbl.name == "minecraft:coal_block" or tbl.name == "minecraft:charcoal_block") then
					fuelCount = tbl.count
					for i = (0-fuelCount),0 do
						if(refueled < arg) then
							turtle.refuel(1)
							refueled = refueled + fuelCost(tbl.name)
						else
							break
						end
					end
				end
			end
		end
		slot = slot + 1
	end
	turtle.select(1);
	if(refueled > 0) then
		return "true"
	else 
		return "false" 
	end
end
 
function parseMsg(fullMsg)
	cnt1 = 0
	msglist = {}
	for token in string.gmatch(fullMsg, "[^%s]+") do
   		msglist[cnt1] = token
   		cnt1 = cnt1 + 1
	end
	msg = msglist[0]
	arg = msglist[1]
    if msg == 'fw' then
        sendString = st1 .. tostring(turtle.forward()) .. st2;
    elseif msg == 'bk' then
        sendString = st1 .. tostring(turtle.back()) .. st2;
    elseif msg == 'rl' then
        sendString = st1 .. tostring(turtle.turnLeft()) .. st2;
    elseif msg == 'rr' then
        sendString = st1 .. tostring(turtle.turnRight()) .. st2;
    elseif msg == 'fuel' then
        sendString = '{"fuelAmount":"' .. tostring(turtle.getFuelLevel()) .. st2;
    elseif msg == 'refuel' then
        sendString = st1 .. autoRefuel(arg) .. st2;
    elseif msg == 'inspectFwd' then
        isBlock, str = turtle.inspect()
        if isBlock then
            sendString = str.name
        else
            sendString = statusNone
        end
    elseif msg == 'mineF' then
    	sendString = st1 .. tostring(turtle.dig()) .. st2
    elseif msg == 'dropAll' then
    	sendString = st1 .. dropAll() .. st2
    else
        return false;
    end
end
 
function connect()
    ws, err = http.websocket(myURL);
    if ws then
        ws.send(sendString);
        sendString = '{"status":"Unknown"}';
        msg = ws.receive();
        response = parseMsg(msg);
        if (response == false) then
            print('> ' .. msg);
        end
        sleep(0.25);
        connect();
    else
        sleep(0.25);
        connect();
    end
end
 
connect();
