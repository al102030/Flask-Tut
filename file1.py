from flask import Flask


app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! this is the main page. <h1>HELLO</h1>"

if __name__ == "__main__":
    app.run() 
