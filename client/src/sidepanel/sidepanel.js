
 

// Variables
var messages = document.querySelector('.message-list')
var btn = document.querySelector('.send-btn')
var input = document.querySelector('input')

btn.addEventListener('click', sendMessage)
input.addEventListener('keyup', function(e){ if(e.keyCode == 13) sendMessage() })

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.buttonClicked) {
    // Button was clicked successfully
    writeLine("Item added to cart", "bot")

  } else {
    // Button was not found
    writeLine("You don't seem to be on a product page", "bot")
    
  }
});

function sendMessage() {
  var msg = input.value;
  input.value = '';
  writeLine(msg, "user");
  var lcMsg = msg.toLowerCase()
  if (lcMsg.includes("cart") && lcMsg.includes("add")) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
          const button = document.querySelector('.dataStreamAddToCart');
          if (button) {
            button.click();
            chrome.runtime.sendMessage({ buttonClicked: true });

          } else {
            chrome.runtime.sendMessage({ buttonClicked: false });
          }
        },
      });
    });
    return
  }
  else if(lcMsg.includes("scroll")) {
    var sections = ['reviews', 'overview', 'layers', 'details', 'specs']
    const matchFound = sections.find(section => lcMsg.includes(section));
    console.log(matchFound)
    if(matchFound) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const newFragment = matchFound;

        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: (newFragment) => {
              window.location.hash = newFragment;
          },
          args: [newFragment],
      });
    });
    } else {
      writeLine("Couldn't find the section in this page", "bot");
    }
    return;
  }

  // Check the cache using the modified checkCache function
  const cachedData = checkCache(msg);
  if (cachedData) {
    // If data is found in the cache, display it
    console.log("Data found in cache");
    writeLine(cachedData, "bot");
  } else {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    const postData = { 'message': msg };

    writeLine('Fetching data...', 'bot');

    fetch(`http://127.0.0.1:5000/`, {
      method: 'POST',
      mode: 'cors',
      headers: headers,
      body: JSON.stringify(postData),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.data);
        replaceLine(data.data, 'bot');
        addToCache(msg, data.data);
      })
      .catch(error => {
        console.error('Error:', error);
        replaceLine('Backend error', 'bot');
      });
  }
}

 
 
function writeLine(text, who){
   var message = document.createElement('li')
   if(who == "user") {
    message.classList.add('message-item', 'item-secondary')
   } else {
    message.classList.add('message-item', 'item-primary')
   }
   message.innerHTML = text
   messages.appendChild(message)
   messages.scrollTop = messages.scrollHeight;
}
function replaceLine(newText, who) {
  var messageItems = document.querySelectorAll('.message-item');
  
  if (messageItems.length > 0) {
     var lastMessage = messageItems[messageItems.length - 1];
     
     // Create a new message element with the updated text
     var newMessage = document.createElement('li');
     newMessage.classList.add('message-item', who === "user" ? 'item-secondary' : 'item-primary');
     newMessage.innerHTML = newText;

     // Replace the last message with the new one
     lastMessage.parentNode.replaceChild(newMessage, lastMessage);

     // Scroll to the bottom of the message container
     messages.scrollTop = messages.scrollHeight;
  }
}

function checkCache(key) {
  const data = localStorage.getItem(key);
  return data;
}

function addToCache(key, data) {
  localStorage.setItem(key, data);
}