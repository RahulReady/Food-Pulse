
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("set").addEventListener("click", popup);
});

function popup() {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    var activeTab = tabs[0];

    var params = {
      "url": "https://ka1brxx1hb.execute-api.us-east-2.amazonaws.com/default?" + "url=" + activeTab.url,
      "method": "POST",
      "timeout": 0,
      "headers": {
        "Content-Type": "application/json"
      },
    };

    $.ajax(params).done( (response) => {
      console.log(response);
      chrome.tabs.sendMessage(activeTab.id, response);
    });

  });
}