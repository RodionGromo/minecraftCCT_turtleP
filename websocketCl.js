let ws = new WebSocket("ws://localhost:9000")
let mainText = document.getElementById('returnText')
let turtlesIDT = document.getElementById('turtlesID')
let turtleIDField = document.getElementById('turtleID')
let commandField = document.getElementById('command')
let selfIdText = document.getElementById('SelfIDText')
let robots = []
let ID = ""
ws.onopen = function(e) {
	console.log("Подключился к бебсокету")
	ws.send('{"message":"socketInfo","who":"comander"}')
	ws.send('{"message":"getRobots"}')
}

ws.onmessage = function(msg) {
	data = JSON.parse(msg.data)
	if(data.message == "returnBots") {
		console.log("Роботов накинули:")
		console.log(data.bots)
		robots = data.bots
		turtlesIDT.innerHTML = beautifyBots();
	} else if(data.message == "logDone") {
		console.log("получил свой ID")
		ID = data.uniqueID
		selfIdText.innerHTML = "Ваш ID:" + ID
	} else if(data.message == "returnValue") {
		console.log("Бот что-то вернул")
		console.log(data.val)
		if(data.infoType == 'state') {
			if(typeof(data.val) == 'string') {
				trueData = eval(data.val)
			} else {
				trueData = data.val
			}
			mainText.innerHTML = "Последнее, что вернул бот: " + trueData
		} else if(data.infoType == 'block') {
			mainText.innerHTML = "Последнее, что вернул бот: " + data.val.name
		} else if(data.infoType == 'crit') {
			mainText.innerHTML = "Ошибка при исполнении команды, возможно неправильная команды"
		} else if(data.infoType == 'stringInfo') {
			if(data.val == "Movement obstructed") {
				mainText.innerHTML = "Движение невозможно"
			} else {
				mainText.innerHTML = "Последнее, что вернул бот: " + data.val
			}
			
		}
	}
}

ws.onclose = function(e) {
	console.log("Вебсокет умрал")
}

function updateRobots() {
	ws.send('{"message":"getRobots"}')
}

function destroyConnection() {
	console.log("закрываю соединение")
	ws.close()
}

function action(act) {
	sendPrebuildCMD("turtle."+act+"()")
}

function actionAdv(advAct) {
	if(advAct == 'nextSlot') {
		sendPrebuildCMD("turtle.select(turtle.getSelectedSlot()+1)")
	} else if(advAct == 'prevSlot') {
		sendPrebuildCMD("turtle.select(turtle.getSelectedSlot()-1)")
	}
}

function beautifyBots() {
	magicString = ""
	for(var i = 0; i < robots.length;i++) {
		magicString += `Бот ${robots[i].id}, топливо: ${robots[i].fuel}<br>`
	}
	return magicString
}

function sendCmd() {
	if(turtleIDField.value == "") {
		alert("Введите ID черепашки")
	} else if(commandField.value == "") {
		alert("Введите команду")
	} else {
		ws.send(`{"message":"newCommand","toID":"${turtleIDField.value}","command":"${commandField.value}","comanderID":"${ID}"}`)
		ws.send('{"message":"getRobots"}')
	}
}

function sendPrebuildCMD(cmd) {
	if(turtleIDField.value == "") {
		alert("Введите ID черепашки")
	} else {
		ws.send(`{"message":"newCommand","toID":"${turtleIDField.value}","command":"${cmd}","comanderID":"${ID}"}`)
		ws.send('{"message":"getRobots"}')
	}
}