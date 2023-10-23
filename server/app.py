from flask import Flask, jsonify, request
from flask_cors import CORS  

from chat import query

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})  # Enable CORS

# on the terminal type: curl http://127.0.0.1:5000
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'GET':
        data = "hello world"
        return jsonify({'data': data})
    elif request.method == 'POST':
        # Assuming the data sent in the POST request is in JSON format
        request_data = request.get_json()
        # Process the data from the POST request
        if 'message' in request_data:
            print(request_data)
            message = request_data['message']
            response = query(message)
            print(response)
            # You can perform additional processing here
            return jsonify({'data': response})
        else:
            return jsonify({'error': 'Invalid POST data'})



# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000/home/10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    return jsonify({'data': num**2})

# driver function
if __name__ == '__main__':
    app.run(debug=True)
