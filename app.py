from flask import Flask, jsonify, render_template, request
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes on the app

# Route to serve the HTML page (for your internal client, if still used)
@app.route("/", methods=["GET"])
def index():
    """
    Handles POST requests to the API endpoint and returns a JSON message.
    This endpoint now allows cross-origin requests due to CORS(app) above.
    """
    if request.is_json:
        data_received = request.get_json()
        print(f"Received data from frontend: {data_received}")

        response_message = "Data successfully processed!"
        if data_received and "name" in data_received:
            response_message = f"Hello, {data_received['name']}! Your data was processed."

        return jsonify({
            "status": "success",
            "message": response_message,
            "received_payload": data_received
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

# API endpoint to handle POST requests
@app.route("/api/submit_data", methods=["POST"])
def submit_data_api():
    """
    Handles POST requests to the API endpoint and returns a JSON message.
    This endpoint now allows cross-origin requests due to CORS(app) above.
    """
    if request.is_json:
        data_received = request.get_json()
        print(f"Received data from frontend: {data_received}")

        response_message = "Data successfully processed!"
        if data_received and "name" in data_received:
            response_message = f"Hello, {data_received['name']}! Your data was processed."

        return jsonify({
            "status": "success",
            "message": response_message,
            "received_payload": data_received
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
