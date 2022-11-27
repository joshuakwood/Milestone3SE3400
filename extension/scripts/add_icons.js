function addIcons(data) {
    var searchResults = document.querySelectorAll(".yuRUbf");

    console.log(data);
    for (let i = 0; i < searchResults.length; i++) {
        var website_url = searchResults[i].querySelector("a").href;
        var website_url = website_url.replace("https://", "");
        var website_url = website_url.split("/")[0];
        var header_Obj = searchResults[i].querySelector("h3");

        var keys = Object.keys(data);

        if (website_url in keys) {
            header_Obj.after("   -   This url is cited");
        } else {
            header_Obj.after("   -   this url is not cited");
        }
    };
};