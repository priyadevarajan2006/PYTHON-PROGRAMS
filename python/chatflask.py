
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chatbot():

    if request.method == "POST":

        msg = request.form["message"].lower()

        if "python" in msg:
            return "Python is powerful!"

        elif "hello" in msg:
            return "Hello Student!"

        else:
            return "I am learning..."

    return """
    <form method='POST'>
        <input type='text' name='message'>
        <button type='submit'>Send</button>
    </form>
    """

app.run(host='0.0.0.0', port=5000, debug=False)

