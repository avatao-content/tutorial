from flask import Flask

from tfwsdk import sdk # If you want to communicate with the TFW from the webservice


app = Flask(__name__)

@app.route('/')
def hello_world():
    sdk.step(2) # Stepping to state 2
    return 'Hello, World!'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=11111)