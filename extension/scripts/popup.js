var createaccount_popup_1 = document.getElementById("createaccount_popup_1");
createaccount_popup_1.addEventListener("click", openCreateAccountPopup);

var createaccount_popup_2 = document.getElementById("createaccount_popup_2");
createaccount_popup_2.addEventListener("click", openCreateAccountPopup);

var login_popup = document.getElementById("login_popup");
login_popup.addEventListener("click", openLoginPopup);

var back_popup_1 = document.getElementById("back_to_popupsettings_1");
back_popup_1.addEventListener("click", backtoPopupSettings);

var back_popup_2 = document.getElementById("back_to_popupsettings_2");
back_popup_2.addEventListener("click", backtoPopupSettings);

var popup_settings = document.getElementById("popup_settings");
var popup_login = document.getElementById("popup_Login");
var popup_createAccount = document.getElementById("popup_createUser");

function openCreateAccountPopup() {
    popup_settings.style.display = "none";
    popup_login.style.display = "none";
    popup_createAccount.style.display = "block";
}

function openLoginPopup() {
    popup_settings.style.display = "none";
    popup_login.style.display = "block";
    popup_createAccount.style.display = "none";
}

function backtoPopupSettings() {
    popup_settings.style.display = "block";
    popup_login.style.display = "none";
    popup_createAccount.style.display = "none";
}

var createUser_submit_popup = document.getElementById("createUser_submit_popup");
createUser_submit_popup.addEventListener("click", createUser);

var login_submit_popup = document.getElementById("login_submit_popup");
login_submit_popup.addEventListener("click", loginSubmit);

checkUserAuthentication();

