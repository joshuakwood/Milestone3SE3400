



function checkUserAuthenticationPopup() {
	var popup_settings = document.getElementById("popup_settings");
	fetch("http://localhost:8080/sessions", {
		credentials: 'include'
	}).then(function(response) {
		console.log("status", response.status);
		if (response.status == 201) {
			// hide login screen and display user settings
			response.json().then(function (data) {
				console.log("User logged in!");
				if (popup_settings) {openPopupSettingsLoggedIn();};
				addIcons(data.doc.websites);
				hideIconGroups(data.doc.user_settings);
				//showSettings(data.doc.user_settings);
			});
		} else {
			// use default data and default settings
			fetch("http://localhost:8080/data", {
						credentials: 'include'
			}).then(function(response) {
				if (response.status == 200) {
					response.json().then(function (data) {
						var defaultSettings = {
							'bias_source': 1,
							'paywall':1,
							'subscription':1,
							'family_friendly':1,
							'ads':1,
							'cyber_safety':1,
							'cookies':1
						};
						console.log("User not logged in!");
						if (popup_settings) {backtoPopupSettings();};
						addIcons(data);
						hideIconGroups(defaultSettings);
					});
				} else {
					console.log("Server Err!");
				};
			}).catch(err => {
				console.log(err);
			});
		};
	}).catch(err => {
		console.log(err);
	});
}


checkUserAuthenticationPopup();