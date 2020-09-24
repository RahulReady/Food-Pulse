
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("set").addEventListener("click", popup);
});

function popup() {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    // Get the currently active tab
    var activeTab = tabs[0];
    // Encore URL so that all special characters are escaped
    var url = encodeURI(activeTab.url);

    console.log(activeTab.url);
    console.log(url);

    // Send GET request to AWS API Gateway
    $.ajax({
      method: "GET",
      url: "https://86e6t1qx46.execute-api.us-east-2.amazonaws.com/v1/reviews",
      data: 
      {
        "url": url
      },
    })
    .done( (response) => {
      console.log(response)
      // Todo: add logic to display the response in the extension popup
    });
  
  });
}