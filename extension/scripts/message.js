function removeMessage() {
	var messageboxes = document.querySelectorAll(".output_message");
	for (var messagebox_i = 0; messagebox_i < messageboxes.length; messagebox_i++) {
	    while (messageboxes[messagebox_i].hasChildNodes()) {
			messageboxes[messagebox_i].removeChild(messageboxes[messagebox_i].firstChild);
		};
	};
}

function createMessage(string, status) {
	console.log(string);
	var messageboxes = document.querySelectorAll(".output_message");
	for (var messagebox_i = 0; messagebox_i < messageboxes.length; messagebox_i++) {
		var message = document.createElement("p");
		message.innerHTML = string;
        if (status == "Bad") {
            message.classList.add("bad_message");
        } else {
            message.classList.add("good_message");
        }
		messageboxes[messagebox_i].appendChild(message);
	};
}