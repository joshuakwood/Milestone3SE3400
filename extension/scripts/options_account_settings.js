
function loadAccountOptions(data) {
    var first_name = data.first_name;
    var last_name = data.last_name;
    var updateAccountInfo = document.querySelector("#update_account_info");
    console.log(updateAccountInfo);
    
    updateAccountInfo.querySelector("#first_name").value = first_name;
    updateAccountInfo.querySelector("#first_name").addEventListener("input", function() {updateAccountInfoButton()})

    updateAccountInfo.querySelector("#last_name").value = last_name;
    updateAccountInfo.querySelector("#last_name").addEventListener("input", function() {updateAccountInfoButton()})

}

function updateAccountInfoButton() {
    var updateAccountButton = document.querySelector("#update_account_submit_button");
    updateSaveButton(updateAccountButton, "clickable");
}

var updateAccountInfo = document.querySelector("#update_account_submit_button");
updateAccountInfo.onclick = function () {
    // get first & last name, & passwords
	var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var new_password = document.getElementById("new_password").value;
    var reenter_password = document.getElementById("reenter_password").value;

    var data = "first_name=" + encodeURIComponent(first_name);
    data = "$last_name=" + encodeURIComponent(last_name);
    data = "$new_password=" + encodeURIComponent(new_password);
	
    fetch("http://localhost:8080/filters", {
        method: "POST",
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
            console.log(response);
            checkUserAuthentication();
        });
}

