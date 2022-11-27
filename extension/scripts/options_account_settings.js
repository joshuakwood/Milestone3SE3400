
function loadAccountOptions(data) {
    var first_name = data.first_name;
    var last_name = data.last_name;
    var updateAccountInfo = document.querySelector("#update_account_info");
    var updateAccountInfoButton = document.querySelector("#update_account_submit_button");
    updateAccountInfoButton.onclick = function () {
        removeMessage();

        // get first & last name
        var first_name = document.getElementById("first_name").value;
        var last_name = document.getElementById("last_name").value;

        var data = "first_name=" + encodeURIComponent(first_name);
        data += "&last_name=" + encodeURIComponent(last_name);
        
        fetch("http://localhost:8080/users/account-settings", {
            method: "PUT",
            credentials: 'include',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
        }).then(function (response) {
            if (response.status == 201) {
                updateSaveButton(updateAccountInfoButton, "off");
                createMessage("Account Settings Saved!", "Good");
                checkUserAuthentication();
            } else {
                createMessage("Changes Not Saved! Try again later!", "Bad");
                checkUserAuthentication();
            };
        });
    };

    updateAccountInfo.querySelector("#first_name").value = first_name;
    updateAccountInfo.querySelector("#first_name").addEventListener("input", function() {updateSaveButton(updateAccountInfoButton, "clickable")})
    updateAccountInfo.querySelector("#last_name").value = last_name;
    updateAccountInfo.querySelector("#last_name").addEventListener("input", function() {updateSaveButton(updateAccountInfoButton, "clickable")})

    var updatePasswordInfo = document.querySelector("#update_password_info");

    updatePasswordInfo.querySelector("#new_password").addEventListener("input", function() {updateSaveButton(newPasswordButton, "clickable")})
    updatePasswordInfo.querySelector("#reenter_password").addEventListener("input", function() {updateSaveButton(newPasswordButton, "clickable")})

    
    var newPasswordButton = document.querySelector("#update_password_submit_button");
    newPasswordButton.onclick = function () {
        console.log("new password clicked");
        removeMessage();

        // get passwords
        var newPassword = document.getElementById("new_password").value;
        var newPasswordRetype = document.getElementById("reenter_password").value;

        if (newPassword != newPasswordRetype) {
            createMessage("Both New Password Entries Must Match!", "Bad");
            checkUserAuthentication();
            return false;
        };

        var data = "new_password=" + encodeURIComponent(first_name);
        
        fetch("http://localhost:8080/users/change-password", {
            method: "PUT",
            credentials: 'include',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
        }).then(function (response) {
            if (response.status == 201) {
                updateSaveButton(newPasswordButton, "off");
                createMessage("New Password Saved!", "Good");
                updatePasswordInfo.querySelector("#new_password").value = "";
                updatePasswordInfo.querySelector("#reenter_password").value = "";
                checkUserAuthentication();
            } else {
                createMessage("Changes Not Saved! Try again later!", "Bad");
                checkUserAuthentication();
            };
        });
    };
};

