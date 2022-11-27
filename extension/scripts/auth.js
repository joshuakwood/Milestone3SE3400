

function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(document.cookie); //to be careful
  const cArr = cDecoded.split('; ');
  let res;
  cArr.forEach(val => {
    if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res
}

var createUserButton = document.querySelector('#createaccount');
createUserButton.onclick = function () {
	document.getElementById("LoginScreen").style.display = 'none';
	document.getElementById("createUserScreen").style.display = 'block';
};

var Back = document.querySelector('#backtoLogin');
backtoLogin.onclick = function () {
	document.getElementById("LoginScreen").style.display = 'block';
	document.getElementById("createUserScreen").style.display = 'none';
};

// load myPeople from a server as JSON data
function checkUserAuthentication() {
	fetch("http://localhost:8080/sessions", {
		credentials: 'include'
	}).then(function(response) {
		console.log("status", response.status);
		console.log("cookies",document.cookie);
		if (response.status == 201) {
			// hide login screen and display data
			document.getElementById("settingsPage").style.display = 'block';
			document.getElementById("LoginScreen").style.display = 'none';
			response.json().then(function (data) {
				loadFilterOptions(data);
				loadAccountOptions(data);
				return data;
			});
		} else if (response.status == 401) {
			// hide data and show login screen
			document.getElementById("settingsPage").style.display = 'none';
			document.getElementById("LoginScreen").style.display = 'block';
			console.log("User not logged in!")
		}
	}).catch(err => {
		console.log(err)
	});
}

// login temp user 
var login_submit = document.querySelector('#login_submit');
login_submit.onclick = loginSubmit;

function loginSubmit () {

	// remove message prompt if there is one
	removeMessage();

	// get email & password
	var login_email = document.getElementById("login_email").value;
	var login_password = document.getElementById("login_password").value;

	// Package and format Data
	var data = "email=" + encodeURIComponent(login_email);
	data += "&password=" + encodeURIComponent(login_password);

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
			createMessage("User Not Logged in!", "Bad");
			checkUserAuthentication();
		} else {
			createMessage("User Does Not Exist!", "Bad");
		}
	}).catch(err => {
		createMessage("User Does Not Exist!", "Bad");
	});
};

var createUser_submit = document.querySelector('#createUser_submit');
createUser_submit.onclick = createUser;

function createUser () {

	// remove message prompt if there is one
	removeMessage();

	// get first and last name, email, and password
	var createUser_firstName = document.getElementById("createUser_firstName").value;
	var createUser_lastName = document.getElementById("createUser_lastName").value;
	var createUser_email = document.getElementById("createUser_email").value;
	var createUser_password = document.getElementById("createUser_password").value;

	// Package and format Data
	var data = "first_name=" + encodeURIComponent(createUser_firstName);
	data += "&last_name=" + encodeURIComponent(createUser_lastName);
	data += "&email=" + encodeURIComponent(createUser_email);
	data += "&password=" + encodeURIComponent(createUser_password);

	// Send data to Server
	fetch("http://localhost:8080/users", {
		method: 'POST',
		credentials: 'include',
		body: data,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		}
	}).then(function (response) {
		// once the server responds, run this function
		if (response.status == 201) {
			createMessage("New User Created!", "Good");
		} else {
			createMessage("User already exists!", "Good");
		}
	}).catch(err => {
		createMessage("User Does Not Exist!", "Bad");
	});;
};

checkUserAuthentication()