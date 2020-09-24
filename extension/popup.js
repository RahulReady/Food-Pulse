
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("set").addEventListener("click", popup);
});

function popup() {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    var activeTab = tabs[0];

    console.log(activeTab.url);

    $.ajax({
      method: "GET",
      url: "https://86e6t1qx46.execute-api.us-east-2.amazonaws.com/v1/reviews?",
      data: {"url": activeTab.url},
    })
    .done( (response) => {
      console.log(response);
      chrome.tabs.sendMessage(activeTab.id, response);
    });
  
  });
}