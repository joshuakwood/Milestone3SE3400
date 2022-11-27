
function getData() {
	fetch("http://localhost:8080/sessions", {
		credentials: 'include'
	}).then(function(response) {
		if (response.status == 201) {
			response.json().then(function (data) {
                addIcons(data.doc.websites);
                //console.log(data.doc.user_settings);
            });
		} else {
			fetch("http://localhost:8080/data", {
				credentials: 'include'
			}).then(function(response) {
				if (response.status == 200) {
					response.json().then(function (data) {
                        addIcons(data);
                    });
				} else {
                    console.log("Server Err!")
                };
			}).catch(err => {
				console.log(err)
			});
		};
	}).catch(err => {
		console.log(err)
	});
    return output_data;
}

getData();

