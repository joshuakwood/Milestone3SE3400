// Initialize button with user's preferred color
let changeColor = document.getElementById("changeColor");

chrome.storage.sync.get("color", ({ color }) => {
    changeColor.style.backgroundColor = color;
});

// When the button is clicked, inject setPageBackgroundColor into current page
changeColor.addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: addIcons,
    });
});

// The body of this function will be executed as a content script inside the
// current page
function addIcons() {

    // Nathaniel Reeves - This code sets every google search result
    // red and adds a ::after tag containing "  -  This is Text"
    // after each search result.  
    //
    // Note: class .DKV0Md is the class every search result
    //       link falls under. this makes them easy to select.
    let searchResults = document.querySelectorAll(".DKV0Md");
    for (let i = 0; i < searchResults.length; i++) {
        searchResults[i].after("   -   This is Text");
        searchResults[i].style.color = "#ff3434";
    }
}