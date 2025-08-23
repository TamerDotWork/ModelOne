from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello_world():
    """
    Handles POST requests to the root URL and returns a JSON message.
    """
    if request.method == "POST":
        return jsonify({"message": "Hello world"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)