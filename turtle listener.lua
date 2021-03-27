print("Don't forget F3 + P!");
local httpServer = 'http://localhost:8000/'
local text = ''
local command
while true do
	http.get(httpServer .. 'put/fuel/' .. tostring(turtle.getFuelLevel()) .. '/')
	text = http.get(httpServer .. 'getCommands')
	text = text.readAll()
	sleep(0.5);
	if(text ~= 'false') then
		command = loadstring(text)
		command()
	end
	sleep(1)
end
