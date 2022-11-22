// trigger initSettingsData funciton on page load
document.addEventListener("DOMContentLoaded", function() {
  initSettingsData();
});

// login temp user 
var login_submit = document.querySelector('#login_submit');
login_submit.onclick = function () {
	// remove user does not exist message if there is one
	var userdoesnotexist = document.getElementById("userdoesnotexist");
	if (userdoesnotexist != null) {
		userdoesnotexist.remove()
	}
	// get email
	var login_email = document.getElementById("login_email").value;
	console.log("login_email query:",login_email);
	// get password
	var login_password = document.getElementById("login_password").value;
	console.log("login_password query:",login_password);


	// Package and format Data
	var data = "email=" + encodeURIComponent(login_email);
	data += "&password=" + encodeURIComponent(login_password);

	console.log("POST request data:", data)

	// Send data to Server
	fetch("http://localhost:8080/sessions", {
		method: 'POST',
		credentials: 'include',
		body: data,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
	}).then(function (response) {
		// once the server responds, run this function
		if (response.status == 201) {
			document.getElementById("login_menu").style.display = 'none';
			checkUserAuthentication();
		} else {
			var login_output = document.getElementById("login_output");
			var userdoesnotexist = document.createElement("p");
			userdoesnotexist.id = "userdoesnotexist";
			userdoesnotexist.innerHTML = "User Does Not Exist!";
			login_output.appendChild(userdoesnotexist);
		}
	}).catch(err => {
		var login_output = document.getElementById("login_output");
		var userdoesnotexist = document.createElement("p");
		userdoesnotexist.id = "userdoesnotexist";
		userdoesnotexist.innerHTML = "User Does Not Exist!";
		login_output.appendChild(userdoesnotexist);
	});
};


// init data function on page load
function initSettingsData() {
    // init button functions
    document.getElementById("delete_button").addEventListener("click", deleteAccount);

    // get data
    loginUser()
    accountData = fetch("http://localhost:8080/sessions").then((response) => {
        return response.json()
    }).then((data) => {
        console.log(data)
    })
  first_name = document.getElementById("first_name");
  first_name.value = "first name test";
};

function deleteAccount() {
    console.log("delete button worked");
};
