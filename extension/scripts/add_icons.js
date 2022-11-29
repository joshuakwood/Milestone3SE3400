
const messages = {
        "ads": {
            'message':"This site is known to use excessive advertisements.",
            'file':"icons/ads_warning_icon.png"
        },
        "cookies": {
            'message':"This site is known to store many cookies containing sensitive personal information.", 
            'file':"icons/cookie.png"
        },
        "paywall": {
            'message':"This site is known to have paywalls.", 
            'file':"icons/paywall_warning_icon.png"
        },
        "bias_source": {
            'message':"This site is known to have extreem bias.", 
            'file':"icons/bias_warning_icon.png"
        },
        "cyber_safety": {
            'message':"This site is known for security risks.", 
            'file':"icons/security_warning_icon.png"
        },
        "subscription": {
            'message':"This site is known for forcing account and/or email subscriptions", 
            'file':"icons/subscription_warning_icon.png"
        },
        "family_friendly": {
            'message':"This site is known to have inappropriate.",
            'file':"icons/pg13_warning_icon.png"
        }
    };

function addIcons(data) {
    console.log(data);

    result_data = [];
    //getTawResult(result_data); TODO:
    getResults(result_data);

    var formatted_filterKeys = prepareFilter(data);
    var filterKeys = Object.keys(data);

    for (var index = 0; index < result_data.length; index++) {
        if (formatted_filterKeys.includes(result_data[index].hostname)) {
            var parent = result_data[index].Obj;
            var formatted_filterKey = formatted_filterKeys.indexOf(result_data[index].hostname);
            var settings_key_index = filterKeys[formatted_filterKey];
            var settings = data[settings_key_index];


            if (settings['ads'] == 1) {
                addIcon(parent, 'ads');
            };
            if (settings['cookies'] == 1) {
                addIcon(parent, 'cookies');
            };
            if (settings['paywall'] == 1) {
                addIcon(parent,'paywall');
            };
            if (settings['bias_source'] == 1) {
                addIcon(parent, 'bias_source');
            };
            if (settings['cyber_safety'] == 1) {
                addIcon(parent, 'cyber_safety');
            };
            if (settings['subscription'] == 1) {
                addIcon(parent, 'subscription');
            };
            if (settings['family_friendly'] == 1) {
                addIcon(parent, 'family_friendly');
            };
        };
    };
};

function hideIconGroups(settings) {
    if (!settings) {
        return null;
    };
    var icon_classes = Object.keys(messages);
    for (var key_i = 0; key_i< icon_classes.length; key_i++) {
        var icon_class = document.querySelector("." + icon_classes[key_i] + "_popup");
        if (icon_class && settings[icon_classes[key_i]] == 1) {
            icon_class.style.display = "inline";
        };
    };
}

function addIcon(Obj, key) {
    var icon_container = Obj.querySelector(".icon_container");
    if (!icon_container) {
        var icon_container = document.createElement("div");
        icon_container.classList.add("icon_container");
        Obj.appendChild(icon_container);
    };
    // create icon
    var icon = document.createElement("img");
    icon.classList.add("icon");
    icon.classList.add("popupsearchicon");
    icon.classList.add(key + "_popup");
    icon.src = chrome.runtime.getURL("style/" + [messages[key].file]);

    // create message
    let message = document.createElement("p");
    message.textContent = messages[key].message;
    message.classList.add("message");

    // create message box
    let messagebox = document.createElement("div");
    messagebox.appendChild(message);
    messagebox.classList.add("popupmessagebox");
    messagebox.id = "messagebox";

    icon.addEventListener("mouseover", mouseOver);
    icon.addEventListener("mouseleave", mouseLeave);

    function mouseOver(e) {
        appearMessagebox();
    }
    function mouseLeave(e) {
        var parent = icon.parentElement;
        var messagebox = parent.querySelector("#messagebox");
        if (messagebox) {
            parent.removeChild(messagebox); 
        };
    }
    function appearMessagebox(e) {
        var parent = icon.parentElement;
        parent.appendChild(messagebox);
    }

    icon_container.appendChild(icon);
}

function isolateHostname(url) {
    if (url) {
        var hostname = new URL(url).hostname;
        return hostname.split(".")[1];
    } else {
        return null;
    };
};

function prepareFilter(data) {
    var keys = Object.keys(data);
    var formatted_keys = [];
    keys.forEach((key) => 
        (formatted_keys.push(key.split(".")[1]))
    )
    return formatted_keys;
}

function getResults(result_data) {
    var searchSection = document.querySelector(".v7W49e");
    if (!searchSection) {
        return null;
    };
    var ResultsObj = searchSection.children;
    for (var i = 0; i < ResultsObj.length; i++) {
        var website_container = ResultsObj[i].querySelector("cite");
        if (website_container) {
            var website_url = website_container.parentElement.textContent;
            var hostname = isolateHostname(website_url);
            if (hostname) {
                var header_Obj = ResultsObj[i].querySelector("cite").parentElement.parentElement.parentElement;
                if (header_Obj) {
                    result_data.push({"hostname":hostname,"Obj":header_Obj});
                };
            };
        };
    };
    return null;
};

function getTawResult(result_data) {
    //TODO: need to fix taw section to get top result adds.
    var tawSection = document.querySelector("#taw");
    if (!tawSection) {
        return null;
    };
    var ResultsObj = tawSection.children;
    for (var i = 0; i < ResultsObj.length; i++) {
        var website_container = ResultsObj[i].querySelector("cite");
        if (website_container) {
            var website_url = website_container.parentElement.textContent;
            var hostname = isolateHostname(website_url);
            if (hostname) {
                var header_Obj = ResultsObj[i].querySelector("cite").parentElement.parentElement.parentElement;
                if (header_Obj) {
                    result_data.push({"hostname":hostname,"Obj":header_Obj});
                };
            };
        };
    };
    return null;
};

