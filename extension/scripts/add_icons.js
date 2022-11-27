
const messages = {
        "ads": "This site is known to use excessive advertisements.", 
        "cookies": "This site is known to store many cookies containing sensitive personal information.", 
        "paywall": "This site is known to have paywalls.", 
        "bias-source": "This site is known to have extreem bias.", 
        "cyber_safety": "This site is known for security risks.", 
        "subscription": "This site is known for forcing account and/or email subscriptions", 
        "family_friendly": "This site is known to have inappropriate."
    };

function addIcons(data) {
    result_data = [];
    getTawResult(result_data);
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
                addIcon(parent, "./style/icons/ads-warning-icon.png",'ads');
            };
            if (settings['cookies'] == 1) {
                addIcon(parent, "./style/icons/cookie.png",'cookies');
            };
            if (settings['paywall'] == 1) {
                addIcon(parent, "./style/icons/paywall-warning-icon.png",'paywall');
            };
            if (settings['bias-source'] == 1) {
                addIcon(parent, "./style/icons/bias-warning-icon.png",'bias-source');
            };
            if (settings['cyber_safety'] == 1) {
                addIcon(parent, "./style/icons/security-warning-icon.png",'cyber_safety');
            };
            if (settings['subscription'] == 1) {
                addIcon(parent, "./style/icons/subscription-warning-icon.png", 'subscription');
            };
            if (settings['family_friendly'] == 1) {
                addIcon(parent, "./style/icons/pg13-warning-icon.png", 'family_friendly');
            };
        };
    };
};

function addIcon(Obj, source, message_key) {
    var icon_container = Obj.querySelector(".icon_container");
    if (!icon_container) {
        var icon_container = document.createElement("div");
        icon_container.classList.add("icon_container");
        Obj.appendChild(icon_container);
    };
    var icon = document.createElement("img");
    icon.src = chrome.runtime.getURL(source);
    icon.style.margin = '0.5em';
    icon.style.width = '28px';
    icon.style.height = '28px';
    icon.style.transition = '300ms';

    let message = document.createElement("p");
    message.textContent = messages[message_key];
    message.style.overflow = 'hidden';
    message.style.whiteSpace = 'wrap';
    message.style.margin = '3px';
    let messagebox = document.createElement("div");
    messagebox.appendChild(message);
    messagebox.style.position = 'relative';
    messagebox.style.backgroundColor = '#ffffff';
    messagebox.style.width = '100px';
    messagebox.style.height = 'fit-content';
    messagebox.style.border = "solid 1px black";
    messagebox.id = "messagebox";

    icon.addEventListener("mouseover", mouseOver);
    icon.addEventListener("mouseleave", mouseLeave);
    icon.addEventListener("click", appearMessagebox);
    icon.addEventListener("click", appearMessagebox);
    function mouseOver(e) {
        icon.style.width = '32px';
        icon.style.height = '32px';
        icon.style.transition = '300ms';
    }
    function mouseLeave(e) {
        icon.style.width = '28px';
        icon.style.height = '28px';
        icon.style.transition = '300ms';
    }
    function appearMessagebox(e) {
        var parent = icon.parentElement;
        parent.appendChild(messagebox);
    }
    document.addEventListener('click', function(event) {
        var isClickInsideElement = icon_container.contains(event.target);
        if (!isClickInsideElement) {
            var parent = icon.parentElement;
            var messagebox = parent.querySelector("#messagebox");
            if (messagebox) {
                parent.removeChild(messagebox); 
            };
        }
    });
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
    var searchSection = document.querySelector("#taw");
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

