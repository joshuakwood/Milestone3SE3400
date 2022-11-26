
function loadFilterOptions(data) {
     var website_settings = data.doc.websites;
     displaySettings(website_settings);

	 var addWebsiteInput = document.querySelector("#add_website");
	 addWebsiteInput.addEventListener("input", function() {updateAddWebsiteFilterButton()})
}

function updateAddWebsiteFilterButton() {
    var updateAccountButton = document.querySelector("#add_website_submit");
    updateSaveButton(updateAccountButton, "clickable");
}

var addWebsiteButton = document.querySelector("#add_website_submit");
addWebsiteButton.onclick = function () {
	removeMessage()
    // get website
	var website = document.getElementById("add_website").value;

    var data = "website=" + encodeURIComponent(website);
	
    fetch("http://localhost:8080/filters", {
        method: "POST",
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
			if (response.status == 201) {
				createMessage("New Filter Added!", "Good");
				checkUserAuthentication();
				var updateAccountButton = document.querySelector("#add_website_submit");
				updateSaveButton(updateAccountButton, "off");
				var addWebsiteInput = document.querySelector("#add_website");
				addWebsiteInput.value = "";
			} else {
				createMessage("New Filter Submission Failed!  Try again later!", "Bad");
			};
        });
}

function deleteWebsiteSetting (website_key) {
	removeMessage()

    var data = "website=" + encodeURIComponent(website_key);
	
    fetch("http://localhost:8080/users/filters", {
        method: "DELETE",
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
            if (response.status == 201) {
				createMessage("Filter Deleted Successfully!", "Good");
				checkUserAuthentication();
			} else {
				createMessage("Filter Deletion Error! Try again later!", "Bad");
			};
        });
}

function displaySettings(data) {
	var website_settings_table = document.querySelector("#website_settings");
	var websites = Object.keys(data);
    var website_settings_table_tbody = website_settings_table.lastChild;
    while (website_settings_table_tbody.lastChild.id !== "tableheader") {
        website_settings_table_tbody.removeChild(website_settings_table_tbody.lastChild);
    };
    
	if (website_settings != null)  {
		for (var web_i = 0; web_i < websites.length; web_i++) {
			// create a new row object
			var row = website_settings_table.insertRow(-1);
			let website = websites[web_i];
			row.id = website;

			// insert webiste name into template
			var website_cell = row.insertCell(0)
			var a = document.createElement("a");
			a.innerHTML = website;
			a.href = website;
			website_cell.style = "text-align: left;";
			website_cell.appendChild(a);
			
			// insert data 

			// ads
			var ads = row.insertCell(-1);
			var ads_input = document.createElement("input");
			ads_input.type = "checkbox";
			ads_input.id = "ads";
			ads_input.addEventListener("click", function() {updateSettingsData(data, website, "ads")});
			if (data[website].ads == 1) {
				ads_input.checked = true;
			};
			ads.appendChild(ads_input);

			// bias-source
			var bias_source = row.insertCell(-1);
			var bias_source_input = document.createElement("input");
			bias_source_input.type = "checkbox";
			bias_source_input.id = "bias_source";
			bias_source_input.addEventListener("click", function() {updateSettingsData(data, website, "bias_source")});
			if (data[website].bias_source == 1) {
				bias_source_input.checked = true;
			};
			bias_source.appendChild(bias_source_input);

			// paywall
			var paywall = row.insertCell(-1);
			var paywall_input = document.createElement("input");
			paywall_input.type = "checkbox";
			paywall_input.id = "paywall";
			paywall_input.addEventListener("click", function() {updateSettingsData(data, website, "paywall")});
			if (data[website].paywall == 1) {
				paywall_input.checked = true;
			};
			paywall.appendChild(paywall_input);

			// family_friendly
			var family_friendly = row.insertCell(-1);
			var family_friendly_input = document.createElement("input");
			family_friendly_input.type = "checkbox";
			family_friendly_input.id = "family_friendly";
			family_friendly_input.addEventListener("click", function() {updateSettingsData(data, website, "family_friendly")});
			if (data[website].family_friendly == 1) {
				family_friendly_input.checked = true;
			};
			family_friendly.appendChild(family_friendly_input);

			// cyber_safety
			var cyber_safety = row.insertCell(-1);
			var cyber_safety_input = document.createElement("input");
			cyber_safety_input.type = "checkbox";
			cyber_safety_input.id = "cyber_safety";
			cyber_safety_input.addEventListener("click", function() {updateSettingsData(data, website, "cyber_safety")});
			if (data[website].cyber_safety == 1) {
				cyber_safety_input.checked = true;
			};
			cyber_safety.appendChild(cyber_safety_input);

			// subscription
			var subscription = row.insertCell(-1);
			var subscription_input = document.createElement("input");
			subscription_input.type = "checkbox";
			subscription_input.id = "subscription";
			subscription_input.addEventListener("click", function() {updateSettingsData(data, website, "subscription")});
			if (data[website].subscription == 1) {
				subscription_input.checked = true;
			};
			subscription.appendChild(subscription_input);

			// cookies
			var cookies = row.insertCell(-1);
			var cookies_input = document.createElement("input");
			cookies_input.type = "checkbox";
			cookies_input.id = "cookies";
			cookies_input.addEventListener("click", function() {updateSettingsData(data, website, "cookies")});
			if (data[website].cookies == 1) {
				cookies_input.checked = true;
			};
			cookies.appendChild(cookies_input);

			// remove button
			var button = row.insertCell(-1);
			var button_input = document.createElement("input");
			var button_container = document.createElement("div");
			button_container.classList.add("button_container")
			button_input.type = "button";
			button_input.classList.add("button");
			button_input.classList.add("on");
			button_input.id = "remove_website";
			button_input.value ="Remove";
            button_input.addEventListener("click", function () {deleteWebsiteSetting(website)});
			button_container.appendChild(button_input);
			button.appendChild(button_container);

		};
        // save button
        var row = website_settings_table.insertRow(-1);
        var button = row.insertCell(-1);
        var button_input = document.createElement("input");
        var button_container = document.createElement("div");
        button_container.classList.add("button_container")
        button_input.type = "button";
        button_input.classList.add("button");
        button_input.classList.add("off");
        button_input.id = "save_website_settings";
        button_input.value ="Save";
        button_input.addEventListener("click", function () {saveWebsiteSetting()});
        button_container.appendChild(button_input);
        button.appendChild(button_container);
	};
}

function updateSettingsData(data, website_key, setting_key) {
	if (data[website_key][setting_key] == 1) {
		data[website_key][setting_key] = 0;
	} else if (data[website_key][setting_key] == 0) {
		data[website_key][setting_key] = 1;
	};
	var website_settings_table = document.querySelector("#website_settings");
	var button = website_settings_table.querySelector("#save_website_settings");
	updateSaveButton(button, "clickable");
    storeWebsiteSettingChanges(data, website_key);
}

// GLOBAL VARIABLE
var settingChanges = {};

function storeWebsiteSettingChanges(data, website_key) {
    var data_update = data[website_key];
	var send_data = "website=" + encodeURIComponent(website_key);
	send_data += "&new_filter_settings=" + encodeURIComponent(JSON.stringify(data_update));
    settingChanges[website_key] = send_data;
}

function saveWebsiteSetting() {
	for (var key in settingChanges) {
		removeMessage()
        var send_data = settingChanges[key];
        
        fetch("http://localhost:8080/users/filter-settings", {
            method: 'PUT',
            credentials: 'include',
            body: send_data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
            console.log(response);
            if (response.status == 201) {
                delete settingChanges[key];
				createMessage("New Filter Settings Saved!", "Good");
                checkUserAuthentication();
            } else {
                createMessage("Save Failed!", "Bad");
            };
        });
    }
}