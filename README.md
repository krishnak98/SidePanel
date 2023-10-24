#### Chrome Sidepanel Chatbot using RAG (Retrieval Augmented Generation)

## Introduction
This repository contains the code and instructions to create a Chrome Sidepanel application that utilizes OpenAI's GPT-3.5 to answer queries about products, using Retrieval Augmented Generation. The application consists of a client-side JavaScript component running within the Chrome browser, and a server-side Python Flask application for handling interactions with the OpenAI API. 
<!-- 
## Setup
1. Create a new extension, by adding the client code to chrome://extensions
2. Install all the required libraries (langchain, openAI, flask, pickle) in the server side code.
2. Ensure you have an OpenAI api key. Add your the key in chat.py
3. Run `python3 app.py`. This will start your server.
4. Go to the website in chrome. Cmd + B opens the sidepanel -->

Installation
Follow these steps to set up the Chrome Sidepanel application:

## 1. Installation

1. Clone the repo
```bash
git clone https://github.com/krishnak98/Sidepanel.git
cd sidepanel
```
2. Install all the required libraries (langchain, openAI, flask, pickle) in the server side code.
3. Ensure you have an OpenAI api key. Add your the key in chat.py
4. Go to chrome://extensions/ in your Chrome browser.
5. Enable "Developer mode" at the top right corner.
6. Click "Load unpacked" and select the client directory.


## 2. Starting the server code
Note: First time you start app.py, it will take about 2 mins to create the vector database
```bash
cd server
python3 app.py
```

This will load and activate the Chrome Sidepanel extension, making it accessible from your Chrome browser. 
Go to your chrome extension, and ask questions, which GPT3.5 will answer, using the data in the URLs you provided.

## 3.Architecture
![Image Alt Text](diagram.png)

Technologies used:
1. LLM -  OpenAI GPT3.5
2. Langchain
3. LocalStorage for client side cache
4. FAISS for vector datastore
5. Javascript for client side code
6. Python Flask for server side code 

## 4. Future Work
1. Add a cache for every userID in the server side, and before querying the LLM, check if they've asked something similar. This cache should store recent interactions and periodically evict older items. However, it's not as easy to implement. if the user asks for a particular product and then asks its price, and then they ask for product 2 and then ask for its price, the second time, it should return the price of the second item, and not the cached price of the first.
2. Improve UI. Currently, you can add items to the cart, and scroll on the same page. But enable going to different pages. If the user asks for a product and asks to go there, we should be able to redirect.