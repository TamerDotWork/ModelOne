from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests if needed (optional)

@app.route("/")
def home():
    return render_template("index.html")  # Flask serves your HTML

@app.route("/api/submit_data", methods=["POST"])
def submit_data():
    try:
        data = request.get_json()
        name = data.get("name")
        value = data.get("value")
        details = data.get("details")
        
        # Example processing
        response_message = f"Received data from {name} with value {value}."
        return jsonify({
            "status": "success",
            "message": response_message,
            "received_data": data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
