
function updateSaveButton(button, state) {
	if (state == "clickable") {
		button.classList.remove("off");
		button.classList.add("on");
	} else {
		button.classList.remove("on");
		button.classList.add("off");
	};
}
