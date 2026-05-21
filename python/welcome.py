from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            return "<h1>Login Successful</h1>"

        return "<h1>Invalid Login</h1>"

    return """
    <html>
    <head>
        <title>Login Page</title>
    </head>

    <body>

        <h2>Flask Login</h2>

        <form method="POST">

            Username:<br>
            <input type="text" name="username"><br><br>

            Password:<br>
            <input type="password" name="password"><br><br>

            <input type="submit" value="Login">

        </form>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)



