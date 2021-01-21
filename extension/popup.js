var AWS = require("aws-sdk");

// On DOM load, setup the following functions
document.addEventListener("DOMContentLoaded", function () {
  listenForRestaurantname();
  onWindowLoad();
  checkCurrentURL();
  window.addEventListener("load", sw.init);
  domElementsSetup();
});

// Listen for content script to send restaurant name
function listenForRestaurantname() {
  chrome.runtime.onMessage.addListener(function (request, sender) {
    if (request.action == "getName") {
      restaurantName.innerText = request.source;
    }
  });
}
// Send the request to execute content.js, which returns the restaurant name to the listenForRestaurantname()
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

// Check if the current url is valid
function checkCurrentURL() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let url = tabs[0].url;
    // If last two chars are double brackets -> give option to proceed
    if (url.slice(-2) === "]]") {
      $("#restaurantName").removeClass("hidden");
      $("#give-me-reviews-button").removeClass("hidden");
      $("#show-me-what-you-got").removeClass("hidden");
      $("#incorrect-url-header").addClass("hidden");
    }
    // Display invalid url message page
    else {
      $("#restaurantName").addClass("hidden");
      $("#incorrect-url-header").removeClass("hidden");
      $("#incorrect-url-rick").removeClass("hidden");
      $("#incorrect-url").removeClass("hidden");
    }
  });
}

/*
Stopwatch code modified from the following link
https://code-boxx.com/simple-javascript-stopwatch/
*/
var sw = {
  // Initialize
  etime: null, // HTML time display
  ego: null, // HTML start/stop button
  init: function () {
    // Get HTML elements
    sw.etime = document.getElementById("sw-time");
    sw.ego = document.getElementById("reviews");
    sw.ego.addEventListener("click", sw.start);
    setTimeout(function () {
      sw.stop;
    }, 4000);
    sw.ego.disabled = false;
  },
  // Timer action
  timer: null, // timer object
  now: 0, // current elapsed time
  tick: function () {
    // Calculate hours, minutes, seconds
    sw.now++;
    var remain = sw.now;
    var hours = Math.floor(remain / 3600);
    remain -= hours * 3600;
    var mins = Math.floor(remain / 60);
    remain -= mins * 60;
    var secs = remain;
    // Update the display timer
    if (hours < 10) {
      hours = "0" + hours;
    }
    if (mins < 10) {
      mins = "0" + mins;
    }
    if (secs < 10) {
      secs = "0" + secs;
    }
    sw.etime.innerHTML = mins + ":" + secs;
  },

  // Start
  start: function () {
    sw.timer = setInterval(sw.tick, 1000);
    // sw.ego.value = "Stop";
    // sw.ego.removeEventListener("click", sw.start);
    // sw.ego.addEventListener("click", sw.stop);
  },
  // Stop
  stop: function () {
    clearInterval(sw.timer);
    sw.timer = null;
  },
};
// Setup the background elements and setup elements on button press
function domElementsSetup() {
  // Redirect to github repo
  $("#help-icon").click(function () {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      var repoURL = "https://github.com/RahulReady/Food-Pulse";
      chrome.tabs.update(tabs.id, { url: repoURL });
    });
  });
  $("#restaurantName").removeClass("hidden");
  $("#waiting-content").hide();
  $("#results-anchor").hide();
  $("#sw-time").hide();
  $(".loader-wrapper").hide();
  // On main button press
  $("#reviews").click(function () {
    $("#show-me-what-you-got").addClass("hidden");
    $("#reviews").hide();
    $("#sw-time").fadeIn();
    $("#waiting-content").fadeIn();
    $(".loader-wrapper").fadeIn();
    // Cloud magic starts here
    callLambdaFunction();
  });
}

// Return the sorted ratings that are greater than the review average for a particular food
function trimSentences(sentences) {
  // Convert all ratings from strings to floats
  map = sentences.map((x) => [x[0], parseFloat(x[1])]);

  // Calculate the average rating
  var avg = map.reduce((sum, val) => sum + val[1], 0) / map.length;

  // Trim all that are below the avg
  var trimmed = map.filter((val) => val[1] >= avg);

  // Sort the array based on the remaining rating values
  trimmed.sort((a, b) => b[1] - a[1]);

  return trimmed;
}

// Create the DOM from the returned Lambda payload
function updateFoodItems(food_items) {
  let apiResult = JSON.parse(food_items);
  console.log(apiResult["food_items"]);
  var elements = document.getElementById("flex-wrapper");
  for (const [key, value] of Object.entries(apiResult["food_items"])) {
    // console.log("value" + value);
    var food = key;
    var sentences = trimSentences(value[2]);

    // Create the buttons
    var g_button_style = document.createElement("div");
    g_button_style.className = "g-button-style";
    g_button_style.textContent = food;
    g_button_style.id = food;

    // Create the button content
    var g_button_content = document.createElement("span");
    g_button_content.className = "hidden";
    sentences.forEach((sent) => {
      var sentence = document.createElement("p");
      sentence.textContent = sent[0] + " " + sent[1] + "/5";
      g_button_content.appendChild(sentence);
      var space = document.createElement("br");
      g_button_content.appendChild(space);
    });

    // Append the button and content to the flex wrapper element
    g_button_style.appendChild(g_button_content);
    elements.appendChild(g_button_style);
  }
  resultButtonActions();
}

// Display lambda results through food-button clicks
function resultButtonActions() {
  $("#results-wrapper").hide();
  var clickedOn = null;
  $(".g-button-style").click(function () {
    let currId = $(this).attr("id");
    if (currId !== clickedOn) {
      // Remove other shaded buttons and shade the currently clicked button
      $(".g-button-style").removeClass("clicked-button");
      $(this).addClass("clicked-button");

      // Take the button content and add it to the results-wrapper
      var content = this.childNodes[1].innerHTML;
      var div = document.getElementById("results-wrapper");
      div.innerHTML = content;
      $("#results-wrapper").fadeIn();
      clickedOn = currId;
    } else {
      $("#results-wrapper").hide();
      $(this).removeClass("clicked-button");
      clickedOn = null;
    }
  });
}

const waiting_content = document.querySelector("#waiting-content");
var done = false;

var earlyMessages = [
  "\"Let's play a game Morty. It's called the waiting game.\" - Alt Rick",
  '"My story begins at the dawn of time in the far away realm of Alphabetrium."<br>- Iced Tea',
  '"And awayyyy we go!"<br>(This sounds familiar)',
  '"And awayyyy we go!"<br>(Rick said this somewhere)',
];
var middleMessages = [
  '"Wubba lubba dub dub!" <br>- AWS Lambda',
  '"If I let you make me nervous, then we can’t get schwifty." - AWS Lambda',
  '"I’m sorry, but your opinion means very little to me." - AWS Lambda',
  '"Lemme check my list of powers and weaknesses: ability to do anything, but only whenever [you] want." - AWS Lambda',
];
var lateMessages = [
  '"When you know nothing matters the universe is yours, and I\'ve never met a universe that was into it." - Rick',
  '"Sometimes science is more art than science, Morty. Lot of people don’t get that." <br>- Rick',
  '"It’s your choice to take [anything] personally." <br>- Rick ',
  '"If I’ve learned one thing, it’s that before you get anywhere in life, you gotta stop listening to yourself." - Jerry',
];

// Display messages during the waiting period
function keepFetchingForMessages() {
  // Set whatever intervals along with what position they should be displayed
  delay(001, 1).then(delay(20600, 2)).then(delay(40800, 3));
}

// Select a random message from a list of 4 messages
function randomNum() {
  return Math.floor(Math.random() * 4);
}

// Display the waiting message at the specified interval
function delay(time, message_place) {
  return new Promise(function (resolve) {
    var timeout = setTimeout(function () {
      if (!done) {
        if (message_place === 1) {
          waiting_content.innerHTML = earlyMessages[randomNum()];
        } else if (message_place === 2) {
          waiting_content.innerHTML = middleMessages[randomNum()];
        } else {
          waiting_content.innerHTML = lateMessages[randomNum()];
        }
        resolve();
      }
    }, time);
  });
}
// Call lambda function with current url and start the waiting messages
function callLambdaFunction() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let url = tabs[0].url;
    const { Secrets } = require("./secrets.js");
    const main = async () => {
      keepFetchingForMessages();
      AWS.config.update({
        // public facing key that has no permissions except invoking the main lambda function
        accessKeyId: Secrets.accessKeyId,
        secretAccessKey: Secrets.secretAccessKey,
        region: Secrets.region,
      });
      const params = {
        FunctionName: Secrets.FunctionName,
        Payload: JSON.stringify({
          params: {
            querystring: {
              url: url,
            },
          },
        }),
      };
      const result = await new AWS.Lambda().invoke(params).promise();
      done = true;

      console.log(result["Payload"]);
      // Check for timeout
      if ("errorMessage" in JSON.parse(result["Payload"])) {
        $("#sw-time").hide();
        $("#restaurantName").hide();
        $(".loader-wrapper").hide();
        $("#waiting-content").hide();
        $("#timeout-message").fadeIn();
        console.log("error!");
      } else {
        $("#sw-time").hide();
        $(".loader-wrapper").hide();
        $("#waiting-content").hide();
        $("#results-anchor").fadeIn();
        updateFoodItems(result["Payload"]);
      }
    };

    main().catch((error) => console.error(error));
  });
}
