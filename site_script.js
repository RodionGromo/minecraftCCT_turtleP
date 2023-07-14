let addr = {
	ip: "10.8.0.3",
	port: 7890
}
let if_robotID = document.getElementById("id_input")
let txt_availableRobots = document.getElementById("available_turtles")
let text_robotFuel = document.getElementById("current_turtle_fuel")
let if_command = document.getElementById("command_input")

async function sendCommand(command, id) {
	return new Promise((resolve, reject) => {
		let request = new XMLHttpRequest;
		request.open("POST", "http://" + addr.ip + ":" + addr.port + "/parseCommand", true)
		request.setRequestHeader("Content-Type", "text/plain;");
		request.send(JSON.stringify({"id": id, "command": command}))
		
		request.onload = function() {
			if(request.status != 200) {
				console.error("command " + command + " returned fail")
				console.log(request.response)
				reject(JSON.parse(request.response));
			} else {
				console.log("command " + command + " - success: ")
				console.log(request.response)
				resolve(JSON.parse(request.response));
			}
		}
	})
}

async function sendCommandWithData(command, id, data) {
	return new Promise((resolve, reject) => {
		let request = new XMLHttpRequest;
		request.open("POST", "http://" + addr.ip + ":" + addr.port + "/parseCommand", true)
		request.setRequestHeader("Content-Type", "text/plain;");
		request.send(JSON.stringify({"id": id, "command": command, "data": data}))
		
		request.onload = function() {
			if(request.status != 200) {
				console.error("command " + command + " returned fail")
				console.log(request.response)
				reject(JSON.parse(request.response));
			} else {
				console.log("command " + command + " - success: ")
				console.log(request.response)
				resolve(JSON.parse(request.response));
			}
		}
	})
}

async function fastCommand(command) {
	turtle_id = Number(if_robotID.value)
	if(turtle_id == 0) {
		alert("Введите ID!")
		return
	}
	sendCommandWithData("turtleCommand", turtle_id, command)
}

async function button_command(command) {
	turtle_id = Number(if_robotID.value)
	let data = await sendCommand("getBot", turtle_id)
	console.log(data)
}

async function send_turtle_command() {
	turtle_id = Number(if_robotID.value)
	command = if_command.value
	if(turtle_id == 0) {
		alert("Введите ID!")
		return
	}
	if(command.length == 0) {
		alert("Введите команду")
		return
	}
	let data = await sendCommandWithData("turtleCommand", turtle_id, command)
	console.log(data)
}

async function preload_turtle() {
	turtle_id = Number(if_robotID.value)
	let data = await sendCommand("getBot", turtle_id)
	text_robotFuel.innerHTML = `Черепашка ${turtle_id} - топливо: ${data.data.fuel} <br>Последняя команда и результат: ${data.data.lastCommand ? data.data.lastCommand : "нет"} - ${data.data.lastData}`;
}

async function get_turtles() {
	let data = await sendCommand("getBots", -1)
	console.log(data)
	if(data == null) {
		console.error("ничего не пришло почему то..")
		return
	}
	magicString = ""
	for(let i = 0; i < data.data.length;i++) {
		magicString += data.data[i].robotID + ", "
	}
	txt_availableRobots.innerHTML = "Доступные роботы: " + magicString
}