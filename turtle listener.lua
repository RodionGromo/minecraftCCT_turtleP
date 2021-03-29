-- pastebin link: https://pastebin.com/ZHwX3w9q
print("Don't forget F3 + P!");
local httpServer = 'http://25.84.31.18:8000/'
local text = ''
local command
local id = ''
local gettingid = false
local botX,botY,botZ = 0
local f = nil
local f2 = nil
local done = false
local registred = false
local dir = ''
function stringifyArray(array)
    string2 = '{'
    for i = 1,#array do
        if(i == #array) then
            string2 = string2 .. array[i]
        else
            string2 = string2 .. array[i] .. ','
        end
    end
    string2 = string2 .. '}'
    return string2
end

function getNormalArrFromPos(x,y,z)
	bstring = '"[' .. tostring(x) .. ',' .. tostring(y) .. ',' .. tostring(z) .. ']"'
	return bstring
end

function getCorrectDir(dir)
	if(dir == 'south') then
		return 'north'
	elseif(dir == 'north') then
		return 'south'
	elseif(dir == 'east') then
		return 'west'
	elseif(dir == 'west') then
		return('east')
	end
end
 
function getId()
    f = io.open('./id.txt','r'):read()
    f2 = io.open('./pos.txt', 'r'):read()
    print(f,f2)
    if(string.find(f,'unknown') ~= nil) then
    	print('starting init')
        tid = string.gsub(f,'unknown ','')
        text = http.get(httpServer .. 'getNewId/' .. tid)
        id = text.readAll()
        print('Done getting new id, please type in:')
        print('X:')
        local posX = read()
        print('Y:')
        local posY = read()
        print('Z:')
        local posZ = read()
        print('Now we need a direction')
        print('Would you do it or automode? (automode requires a furnace in first slot)')
        print('type "manual" or "auto"')
        answ = read()
        if(answ == 'auto') then
        	turtle.select(1)
        	item = ''
        	print('awaiting furnace')
        	while item ~= 'minecraft:furnace' do
        		tbl = turtle.getItemDetail()
        		item = tbl.name
        		sleep(1)
        	end
        	turtle.place()
        	isBlock,tbl = turtle.inspect()
        	sleep(0.1)
        	dir = getCorrectDir(tbl.state.facing)
        else
        	print('type south, east, west, north')
        	dir = read()
        	if(dir ~= 'south' or dir ~= 'east' or dir ~= 'west' or dir ~= 'north') then
        		error('invalid direction',0)
        	end
        end
        print("For the safety: is everything right?")
        print("ID is: " .. id)
        print("Current pos is: X:" .. posX .. " Y:" .. posY .. " Z:" .. posZ .. ' D: ' .. dir)
        print('Type y if yes, n if wrong')
        answ = read()
        local newArray = {posX,posY,posZ,dir}
        if(answ == 'y') then
        	io.open('./id.txt','w'):write(id)
        	io.open('./pos.txt','w'):write(stringifyArray(newArray))
    	else
    		error('User abort: retry',0)
    	end
    else
    	print('skipped init')
        id = f
        str1 = loadstring('return ' .. f2)
        sleep(0.5)
        str2 = str1()
        botX = str2[1]
        botY = str2[2]
        botZ = str2[3]
        dir = str2[4]
    end
    return true
end
 
while true do
    if(gettingid == false) then
        gettingid = true;
        done = getId()
    end
    if(done == true and registred == false) then
    	text = http.get(httpServer .. 'register/'.. id .. "/" .. botX .. '/' .. botY .. '/' .. botZ .. "/" .. dir)
    	if(text.readAll() == 'ok') then
    		registred = true;
    	else
    		registred = true;
    	end
    end
    if(id.len(id) == 4 and done == true and registred == true) then
    	shell.run("http.get(httpServer .. 'put/fuel/' .. turtle.getFuelLevel() .. '/' .. id)")
 		text = http.get(httpServer .. 'getCommands/' .. id)
 		print('await') 
 		msg = text.readAll()
 		print(msg)
 		success,msg1,msg2 = pcall(loadstring(msg))
 		if(success == true) then
 			print('got a runnable command')
 			if(msg2 ~= nil) then
 				print('got a msg2 table')
 				if(type(msg2) == 'table') then
 					http.get(httpServer .. '/' .. msg2.name .. '/' .. id)
 				end
 			else
 				print('sent a msg1')
 				http.get(httpServer .. '/' .. msg1 .. '/' .. id)
 			end
 		end
    end
end
