from flask import Flask, jsonify, request
from flask_cors import CORS  
import os
from chat import queryGPT, create_vectorized_store

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})  # Enable CORS

# on the terminal type: curl http://127.0.0.1:5000
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        request_data = request.get_json()
        # Process the data from the POST request
        if 'message' in request_data:
            message = request_data['message']
            response = queryGPT(message)
            print(response)
            # You can perform additional processing here
            return jsonify({'data': response})
        else:
            return jsonify({'error': 'Invalid POST data'})


# driver function
if __name__ == '__main__':
    if not os.path.exists('faiss_store_openai.pkl'):
        create_vectorized_store()
    
    app.run(debug=True)
