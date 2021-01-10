var AWS = require("aws-sdk");

// listen for content script to send restaurant name
chrome.runtime.onMessage.addListener(function (request, sender) {
  if (request.action == "getName") {
    restaurantName.innerText = request.source;
  }
});

document.addEventListener("DOMContentLoaded", function () {
  // On window load display restaurant name from content DOM
  window.onload = onWindowLoad;

  $(document).ready(function () {
    $("#results-anchor").hide();
    $(".loader-wrapper").show().delay(1000).hide();

    $("#reviews").click(function () {
      $("#reviews").hide();
      $(".loader-wrapper").show();
      stop();
      startstuff();
    });
  });
  // document.getElementById("reviews").addEventListener("click", tests);
  document
    .getElementById("reviews")
    .addEventListener("click", callLambdaFunction);
});

function startstuff() {
  setTimeout(function () {
    $("#results-anchor").show();
  }, 2000);
}

function stop() {
  setTimeout(function () {
    $(".loader-wrapper").hide();
  }, 2000);
}

function onWindowLoad() {
  var restaurantName = document.querySelector("#restaurantName");
  chrome.tabs.executeScript(
    null,
    {
      file: "content.js",
    },
    function () {
      // If you try and inject into an extensions page or the webstore/NTP you'll get an error
      if (chrome.runtime.lastError) {
        message.innerText =
          "There was an error injecting script : \n" +
          chrome.runtime.lastError.message;
      }
    }
  );
}

// // Initialize Tabs in Popup
// $(document).ready(function () {
//   $(".tabs").tabs();
// });

function tests(food_items) {
  // food_items = '{"food_items":{"turkey":0.3, "taco":0.8, "sandwich":0.1} }';
  // {"food_items": {"fish": [0.7213529146634615, 3], "…40624999, 2]}, "restaurant_name": "Poke Bowl Co"}"
  let apiResult = JSON.parse(food_items);
  console.log(apiResult["food_items"]);
  var elements = document.getElementById("food-item-list");
  for (const [key, value] of Object.entries(apiResult["food_items"])) {
    var food = key;

    var sentences = value[2];
    sentences.map( (sent) => {
      return "' " + sent + " '";
    }).join('\n');

    var list_item = document.createElement("li");
    var div1 = document.createElement("div");
    div1.className = "collapsible-header";
    div1.textContent = food;

    var div2 = document.createElement("div");
    div2.className = "collapsible-body";
    div2.textContent = sentences;

    list_item.appendChild(div1);
    list_item.appendChild(div2);
    elements.appendChild(list_item);
  }
}

function callLambdaFunction() {
  console.log("came here");
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let url = tabs[0].url;
    url = encodeURI(url);
    // console.log(url);
 
    // let url = "bleh";
    const main = async () => {
      // http://docs.aws.amazon.com/AWSJavaScriptSDK/guide/node-configuring.html
      AWS.config.update({
        // public facing key that has no permissions except invoking the main lambda function
        accessKeyId: "",
        secretAccessKey: "",
        region: "",
      });
      const params = {
        FunctionName: "",
        Payload: JSON.stringify({
          params: {
            querystring: {
              url: url,
            },
          },
        }),
      };
      const result = await new AWS.Lambda().invoke(params).promise();
      console.log("Success!");
      console.log(result["Payload"]);
      console.log(tests(result["Payload"]));
      // console.log(tests(result));
    };

    main().catch((error) => console.error(error));
  });
}
