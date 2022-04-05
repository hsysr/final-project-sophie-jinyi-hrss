from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def status():
    """Server status route

    The function implement the root route and returns
    "Server On" if the server is on

    :param: None

    :returns: None
    """
    return "Server On"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
