// Return restaurant name
function getRestaurantname(document_root) {
  return document_root.getElementsByClassName("P5Bobd")[0].innerText;
}

chrome.runtime.sendMessage({
  action: "getName",
  source: getRestaurantname(document),
});
