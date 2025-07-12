from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# In-memory store of IPs and timestamps
request_log = {}

# Rate limit settings
RATE_LIMIT = 5  # max requests
TIME_WINDOW = 10  # seconds

@app.route("/")
def index():
    ip = request.remote_addr
    current_time = time.time()

    if ip not in request_log:
        request_log[ip] = []

    # Remove timestamps older than TIME_WINDOW
    request_log[ip] = [timestamp for timestamp in request_log[ip] if current_time - timestamp < TIME_WINDOW]

    if len(request_log[ip]) >= RATE_LIMIT:
        return jsonify({"error": "Rate limit exceeded"}), 429

    request_log[ip].append(current_time)
    return jsonify({"message": "Request accepted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
