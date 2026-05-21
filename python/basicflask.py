from flask import Flask

app = Flask(__name__)

@app.route("/api")
def api():
    return {
        "name": "Hackup",
        "course": "Python"
    }
app.run(host='0.0.0.0', port=9090, debug=False)



