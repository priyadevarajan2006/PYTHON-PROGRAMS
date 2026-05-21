from flask import Flask, request
import webbrowser
import threading

app = Flask(__name__)

students = {}

@app.route('/')
def home():

    return """
    <html>

    <head>
        <title>Student Management System</title>
    </head>

    <body>

    <h1>Student Management System</h1>

    <hr>

    <h2>Add Student</h2>

    <form action="/add" method="post">

        Student Name:
        <input type="text" name="name">

        <br><br>

        Student Mark:
        <input type="number" name="mark">

        <br><br>

        <input type="submit" value="Add Student">

    </form>

    <hr>

    <h2>Search Student</h2>

    <form action="/search" method="post">

        Student Name:
        <input type="text" name="name">

        <br><br>

        <input type="submit" value="Search Student">

    </form>

    <hr>

    <a href="/show">Show All Students</a>

    </body>

    </html>
    """

@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    mark = request.form['mark']

    students[name] = mark

    return f"""
    <h2>Student Added Successfully</h2>

    <p>Name : {name}</p>

    <p>Mark : {mark}</p>

    <br>

    <a href="/">Go Back</a>
    """

@app.route('/search', methods=['POST'])
def search_student():

    name = request.form['name']

    if name in students:

        return f"""
        <h2>Student Found</h2>

        <p>Name : {name}</p>

        <p>Mark : {students[name]}</p>

        <br>

        <a href="/">Go Back</a>
        """

    else:

        return """
        <h2>Student Not Found</h2>

        <br>

        <a href="/">Go Back</a>
        """

@app.route('/show')
def show_students():

    output = "<h2>All Students</h2><hr>"

    if len(students) == 0:

        output += "<p>No Students Added</p>"

    else:

        for name, mark in students.items():

            output += f"""
            <p>
            Name : {name}<br>
            Mark : {mark}
            </p>
            <hr>
            """

    output += '<a href="/">Go Back</a>'

    return output

def open_browser():
    webbrowser.open_new("http://127.0.0.1:9090")

if __name__ == '__main__':

    threading.Timer(1, open_browser).start()

    app.run(host='127.0.0.1', port=9090)
