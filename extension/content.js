// Listen for messages
chrome.runtime.onMessage.addListener( (request, sender, sendResponse) => {
  console.log(request);
});