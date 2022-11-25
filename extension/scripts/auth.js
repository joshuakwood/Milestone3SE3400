// trigger initSettingsData funciton on page load
document.addEventListener("DOMContentLoaded", function() {
  fetchDefaultData();
});

function fetchDefaultData() {
	fetch("http://localhost:8080/data", {
		credentials: 'include'
	}).then(function(response) {
			console.log("status", response.status);
			console.log("cookies",document.cookie);
			if (response.status == 200) {
					// hide login screen and display data
					// document.getElementById("Datapage").style.display = 'block';
					// document.getElementById("LoginScreen").style.display = 'none';
				response.json().then(function (data) {
					showIcons(data);  // Output data onto Document 
				});
			} else if (response.status == 401) {
					// hide data and show login screen
					// document.getElementById("Datapage").style.display = 'none';
					// document.getElementById("LoginScreen").style.display = 'block';
					console.log("User not logged in!")
					console.log(response.statusText)
			}
		}).catch(err => {
			console.log(err)
		});
}

function showIcons(data) {
	// TODO: output data to google search results
	console.log("Data from Server:", data);
}

// load myPeople from a server as JSON data
function checkUserAuthentication() {
	fetch("http://localhost:8080/data", {
		credentials: 'include'
	}).then(function(response) {
			console.log("status", response.status);
			console.log("cookies",document.cookie);
			if (response.status == 200) {
				// hide login screen and display data
				// document.getElementById("Datapage").style.display = 'block';
				// document.getElementById("LoginScreen").style.display = 'none';
		response.json().then(function (data) {
		console.log("Data from Server:", data);
		SERVER_DATA = data;
		// TODO: create a new function to replace printServerData
		// 	   that puts icons on the screen by google search results
		printServerData();  // Output data onto Document 
		});
			} else if (response.status == 401) {
				// hide data and show login screen
				// document.getElementById("Datapage").style.display = 'none';
				// document.getElementById("LoginScreen").style.display = 'block';
				console.log("User not logged in!")
				console.log(response.statusText)
			}
		}).catch(err => {
			console.log(err)
		});
}

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
			var login_output = document.getElementById("login_output");
			var loggedin = document.createElement("p");
			loggedin.id = "userloggedin";
			loggedin.innerHTML = "User is Logged in!";
			login_output.appendChild(loggedin);
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

function deleteAccount() {
    console.log("delete button worked");
};
