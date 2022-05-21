from flask import Flask, request, Response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="" method="post">
        <input type='text' name='input'>
        <input type='submit' value='Submit'>
    </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handler():
    if request.method == 'GET':
        return HTML
    elif request.method == 'POST':
        response = request.form.get('input')
        return f'<h1>{response}</h1>'


@app.after_request
def add_cors(response: Response):
    response.headers['Content-Security-Policy'] = "script-src 'none'"
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
