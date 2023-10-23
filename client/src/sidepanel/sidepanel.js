
 

// Variables
var messages = document.querySelector('.message-list')
var btn = document.querySelector('.btn')
var input = document.querySelector('input')

// Button/Enter Key
btn.addEventListener('click', sendMessage)
input.addEventListener('keyup', function(e){ if(e.keyCode == 13) sendMessage() })


// function sendMessage() {
//    var msg = input.value;
//    input.value = '';
//    writeLineFromUser(msg);
//    console.log(msg);
//    const headers = new Headers();

//    // Send a GET request to your Flask API
//    fetch('http://127.0.0.1:5000/', { method: 'GET', mode: 'cors',headers:headers })
//      .then(response => response.json()) // Parse response as JSON
//      .then(data => {
//        console.log(data.data); // Access the data in the JSON response
//        writeLineFromBot(data.data); // Display the response in your chat
//      })
//      .catch(error => {
//        console.error('Error:', error);
//      });
//  }

 function sendMessage() {
   var msg = input.value;
   input.value = '';
   writeLineFromUser(msg);
   const headers = new Headers();
   const postData = { 'message': msg };
   headers.append('Content-Type', 'application/json');

   
   fetch(`http://127.0.0.1:5000/`, {
      method: 'POST',
      mode: 'cors',
      headers: headers,
      body: JSON.stringify(postData),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.data);
        writeLineFromBot(data.data);
      })
      .catch(error => {
        console.error('Error:', error);
        writeLineFromBot('Backend error');
      });
 }

 
 
function writeLineFromUser(text){
   var message = document.createElement('li')
   message.classList.add('message-item', 'item-secondary')
   message.innerHTML = text
   messages.appendChild(message)
   messages.scrollTop = messages.scrollHeight;
}
function writeLineFromBot(text){
   var message = document.createElement('li')
   message.classList.add('message-item', 'item-primary')
   message.innerHTML =  text
   messages.appendChild(message)
   messages.scrollTop = messages.scrollHeight;
}