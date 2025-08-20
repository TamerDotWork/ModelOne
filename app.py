from flask import Flask, jsonify, render_template, request

# Initialize the Flask application
# The __name__ argument helps Flask find static files and templates
app = Flask(__name__)

# --- Routes ---

@app.route("/", methods=["GET"])
def index():
    """
    Handles GET requests to the root URL ("/").
    This route serves the main HTML page (index.html) to the user's browser.
    """
    # render_template looks for HTML files in the 'templates' folder by default
    return render_template("index.html")

@app.route("/api/submit_data", methods=["POST"])
def submit_data_api():
    """
    Handles POST requests to the "/api/submit_data" endpoint.
    This is your API endpoint that the frontend (AJAX) will call.
    It expects a JSON payload and returns a JSON response.
    """
    # Check if the request body is JSON
    if request.is_json:
        # Get the JSON data from the request body
        data_received = request.get_json()
        print(f"Received data from frontend: {data_received}")

        # You can process the received data here.
        # For this example, we'll just send back a success message
        # along with some acknowledgment of the received data.
        response_message = "Data successfully processed!"
        if data_received and "name" in data_received:
            response_message = f"Hello, {data_received['name']}! Your data was processed."

        # Return a JSON response with a success message and HTTP status 200 (OK)
        return jsonify({
            "status": "success",
            "message": response_message,
            "received_payload": data_received # Echo back the received data
        }), 200
    else:
        # If the request body is not JSON, return an error
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400 # Bad Request status

# --- Application Entry Point ---

if __name__ == "__main__":
    # When running with Docker, host="0.0.0.0" makes the server accessible
    # from outside the container, allowing your browser to connect.
    # debug=True enables auto-reloading of the server on code changes
    # and provides more detailed error messages, which is useful for development.
    app.run(host="0.0.0.0", port=5000, debug=True)
