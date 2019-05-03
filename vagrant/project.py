from flask import Flask     # Flask class from flask library
app = Flask(__name__)       # create instance of class with name of application

@app.route('/')             # decorator - if either routes (/ or /hello) entered into browser
@app.route('/hello')        # function HelloWorld will run.
def HelloWorld():
    return "Hello World"

if __name__ == '__main__':  # if executing from python interpreter run normally on port 5000
    app.debug = True        # server reloads anytime code changes
    app.run(host = '0.0.0.0', port = 5000)
