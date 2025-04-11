# === OpenAlgo Python Server (Port 5000) ===
# Flask server to receive trading signals from AFL and execute via broker API

from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)

# === Broker API Configuration from Environment ===
BROKER_API_KEY = os.getenv("BROKER_API_KEY", "demo_key")
BROKER_CLIENT_ID = os.getenv("BROKER_CLIENT_ID", "demo_client")
BROKER_BASE_URL = os.getenv("BROKER_BASE_URL", "http://localhost:5001")  # Flattrade or local server gateway

# === Trade Execution Function ===
def place_order(signal):
    if signal not in ["CALL_BUY", "PUT_BUY", "EXIT"]:
        return {"status": "error", "msg": "Invalid signal value"}

    data = {
        "client_id": BROKER_CLIENT_ID,
        "api_key": BROKER_API_KEY,
        "order_type": "BUY" if signal in ["CALL_BUY", "PUT_BUY"] else "EXIT",
        "symbol": "BANKNIFTY" if signal.startswith("CALL") or signal.startswith("PUT") else "",
        "option_type": "CE" if signal == "CALL_BUY" else "PE" if signal == "PUT_BUY" else "",
        "product": "MIS",
        "qty": 25,
        "price": 0,
        "type": "MARKET"
    }
    try:
        response = requests.post(f"{BROKER_BASE_URL}/api/v1/order", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "failed", "msg": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"status": "error", "msg": str(e)}

# === Flask Endpoint ===
@app.route("/trade", methods=["POST"])
def trade():
    try:
        signal = request.json.get("signal")
        if not signal:
            return json.dumps({"status": "error", "msg": "Missing signal key in request."})
        result = place_order(signal)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "msg": str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
