from flask import Flask, jsonify, request
from flask_cors import CORS  
import os, time
from chat import queryLLM, create_vectorized_store

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})  # Enable CORS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        request_data = request.get_json()
        # Process the data from the POST request
        if 'message' in request_data:
            message = request_data['message']
            print(message)
            response = queryLLM(message)
            return jsonify({'data': response})
        else:
            return jsonify({'error': 'Invalid POST data'})
    else:
        return jsonify({"data": "hello"})


# driver function
if __name__ == '__main__':
    if not os.path.exists('faiss_store_openai.pkl'):
        create_vectorized_store()
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)

