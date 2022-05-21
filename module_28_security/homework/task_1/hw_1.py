from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handler():
    if request.method == 'GET':
        return jsonify({"Hello": "User"})
    elif request.method == 'POST':
        return jsonify({"Response": "For post"})
    elif request.method == 'PUT':
        return jsonify({"Response": "Updating something"})
    else:
        return jsonify({"Response": "Deleting something"})


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://deep-purple.ru'
    response.headers['Access-Control-Allow-Methods'] = 'DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'

    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
