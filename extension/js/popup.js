document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("test").addEventListener("click", popup);
});

// Initialize Tabs in Popup
$(document).ready(function () {
  $(".tabs").tabs();
});

function popup() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let activeTab = tabs[0].url;

    document.getElementById("before").innerHTML = activeTab;
    url = encodeURI(activeTab);
    document.getElementById("restaurantName").innerHTML = url;
  });
}

function popup1() {
  console.log("here");
  // Only seems to work when app is 'deployed'?
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    // Get the currently active tab
    let activeTab = tabs[0].url;
    // Encore URL so that all special characters are escaped
    // var url = encodeURI(activeTab.url);

    // console.log(activeTab.url);
    // console.log(url);
    document.getElementById("restaurantName").innerHTML = url;

    // Send GET request to AWS API Gateway
    // $.ajax({
    //   method: "GET",
    //   url: "https://86e6t1qx46.execute-api.us-east-2.amazonaws.com/v1/reviews",
    //   data: {
    //     url: url,
    //   },
    // }).done((response) => {
    //   console.log(response);
    //   // Todo: add logic to display the response in the extension popup
    // });
  });
}
