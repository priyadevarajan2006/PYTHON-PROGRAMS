
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def marks():

    if request.method == "POST":

        m1 = int(request.form["m1"])
        m2 = int(request.form["m2"])

        total = m1 + m2

        return f"Total Marks: {total}"

    return """
    <form method='POST'>
        Mark1: <input type='number' name='m1'><br><br>
        Mark2: <input type='number' name='m2'><br><br>
        <button type='submit'>Calculate</button>
    </form>
    """
app.run(host='0.0.0.0', port=5000, debug=False)
