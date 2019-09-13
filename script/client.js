"use strict";
let animationEndClasses = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
let showCaster = (data) => {
	console.log(data);
	console.log(settings);
	$("#alert")
		.queue(() => {
			$("#name").html(data.user.toUpperCase());
			$("#logo img").attr("src", data.image);
			$("#link").html("https://www.twitch.tv/" + data.user);
			if(settings.InSound && settings.PlaySound) {
				$("#sound embed").attr("src", settings.InSound);
			}

			$("#alert")
				.removeClass()
				.addClass(`${settings.InTransition} animated`)
				.one(animationEndClasses, function () {
					$(this)
						.off(animationEndClasses)
						.removeClass()
						.addClass(`${settings.AttentionAnimation} animated`)
						.one(animationEndClasses, function () {
							$(this)
								.removeClass();
						});
				})
				.dequeue();
		})
		.delay((settings.Duration || 10) * 1000)
		.queue(() => {
			if (settings.OutSound && settings.PlaySound) {
				$("#sound embed").attr("src", settings.OutSound);
			}
			$("#alert")
				.removeClass()
				.off(animationEndClasses)
				.addClass(`${settings.AttentionAnimation} animated`)
				.one(animationEndClasses, function () {
					$(this)
						.removeClass()
						.addClass(`${settings.OutTransition} animated`)
						.one(animationEndClasses, function () {
							$(this)
								.removeClass().addClass("hidden");
						});
				})
				.dequeue();
		});
}

let initializeUI = () => {
	$(":root")
		.css("--link-color", `${settings.LinkColor || "rgba(230,126,34,1)"}`)
		.css("--name-color", `${settings.NameColor || "rgba(255, 0, 0, 1)"}`);

	$("#logo img").removeClass().addClass(`${settings.ImageShape} ${settings.EnableShadow ? "shadow" : ""}`);
	$("#name, #link").removeClass().addClass(`${settings.EnableShadow ? "shadow" : ""}`);
};

let connectWebsocket = () => {
	console.log("connect");
	//-------------------------------------------
	//  Create WebSocket
	//-------------------------------------------
	let socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");

	//-------------------------------------------
	//  Websocket Event: OnOpen
	//-------------------------------------------
	socket.onopen = function () {
		console.log("open");
		// AnkhBot Authentication Information
		let auth = {
			author: "DarthMinos",
			website: "darthminos.tv",
			api_key: API_Key,
			events: [
				"EVENT_SO_SETTINGS",
				"EVENT_SO_COMMAND"
			]
		};

		// Send authentication data to ChatBot ws server

		socket.send(JSON.stringify(auth));
	};

	//-------------------------------------------
	//  Websocket Event: OnMessage
	//-------------------------------------------
	socket.onmessage = (message) => {
		console.log(message);
		// Parse message
		let socketMessage = JSON.parse(message.data);
		let eventName = socketMessage.event;
		console.log(socketMessage);
		let eventData = typeof socketMessage.data === "string" ? JSON.parse(socketMessage.data || "{}") : socketMessage.data;
		switch (eventName) {
			case "EVENT_SO_COMMAND":
				$.ajax({
					type: 'GET',
					url: 'https://decapi.me/twitch/avatar/' + eventData.user,
					success: function (data) {
						if (data) {
							showCaster({ user: eventData.user, image: data });
						}
					}
				});

				break;
			case "EVENT_SO_SETTINGS":
				window.settings = eventData;
				if (validateInit()) {
					initializeUI();
				}
				break;
			default:
				console.log(eventName);
				break;
		}
	};

	//-------------------------------------------
	//  Websocket Event: OnError
	//-------------------------------------------
	socket.onerror = (error) => {
		console.error(`Error: ${error}`);
	};

	//-------------------------------------------
	//  Websocket Event: OnClose
	//-------------------------------------------
	socket.onclose = () => {
		console.log("close");
		// Clear socket to avoid multiple ws objects and EventHandlings
		socket = null;
		// Try to reconnect every 5s
		setTimeout(() => connectWebsocket(), 5000);
	};

};

let validateSettings = () => {
	let hasApiKey = typeof API_Key !== "undefined";
	let hasSettings = typeof settings !== "undefined";

	return {
		isValid: hasApiKey && hasSettings,
		hasSettings: hasSettings,
		hasApiKey: hasApiKey
	};
};

let validateInit = () => {
	// verify settings...
	let validatedSettings = validateSettings();

	// Connect if API_Key is inserted
	// Else show an error on the overlay
	if (!validatedSettings.isValid) {
		$("#config-messages").removeClass("hidden");
		$("#config-messages .settings").removeClass(validatedSettings.hasSettings ? "valid" : "hidden");
		$("#config-messages .api-key").removeClass(validatedSettings.hasApiKey ? "valid" : "hidden");
		return false;
	}
	return true;
};

jQuery(document).ready(() => {
	if (validateInit()) {
		initializeUI();
		connectWebsocket();
	} else {
		console.log("Invalid");
	}
});
