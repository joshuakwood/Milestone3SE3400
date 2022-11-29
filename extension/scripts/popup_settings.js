

var ads_toggle = document.getElementById("ads_toggle");
ads_toggle.addEventListener("click", toggleIcon);

var bias_toggle = document.getElementById("bias_toggle");
bias_toggle.addEventListener("click", toggleIcon);

var paywall_toggle = document.getElementById("paywall_toggle");
paywall_toggle.addEventListener("click", toggleIcon);

var security_toggle = document.getElementById("security_toggle");
security_toggle.addEventListener("click", toggleIcon);

var family_friendly_toggle = document.getElementById("family_friendly_toggle");
family_friendly_toggle.addEventListener("click", toggleIcon);

var subscription_toggle = document.getElementById("subscription_toggle");
subscription_toggle.addEventListener("click", toggleIcon);

var cookie_toggle = document.getElementById("cookie_toggle");
cookie_toggle.addEventListener("click", toggleIcon);

var setting_switches = [
    ads_toggle, 
    bias_toggle, 
    paywall_toggle, 
    security_toggle, 
    family_friendly_toggle, 
    subscription_toggle, 
    cookie_toggle
]

function showSettings(settings) {
	console.log(settings);
    for (var i=0; i < settings.length; i++) {
        if (settings[i] == 1) {
            setting_switches[i].checked = true;
        } else {
            setting_switches[i].checked = false;
        };
    };
}

function toggleIcon() {
    state = {};
    for (var i=0; i < setting_switches.length; i++) {
        if (setting_switches[i].checked == true) {
            state[setting_switches[i].id.replace("_toggle","")] = 1;
        } else {
            state[setting_switches[i].id.replace("_toggle","")] = 0;
        };
    };
    saveFilterSetting(state);
}

function saveFilterSetting(state) {

    removeMessage();

    var data =  "filters=" + encodeURIComponent(JSON.stringify(state));
    
    fetch("http://localhost:8080/users/filter-settings", {
        method: 'PUT',
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        console.log(response);
        if (response.status == 201) {
            createMessage("New Filter Settings Saved!", "Good");
            checkUserAuthenticationPopup();
        } else {
            createMessage("Not Signed In", "Bad");
        };
    });
}