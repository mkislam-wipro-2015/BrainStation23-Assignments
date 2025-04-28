from flask import Flask, jsonify
import requests
import socket
from datetime import datetime
import os

app = Flask(__name__)

# Get Version from environment variable
VERSION = os.getenv('VERSION', '1.0.0')

# Weather API URL (Example: Open-Meteo API, free)
WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude=23.8103&longitude=90.4125&current_weather=true"

@app.route('/api/hello', methods=['GET'])
def hello():
    try:
        weather_response = requests.get(WEATHER_API, timeout=5)
        weather_data = weather_response.json()
        temperature = weather_data['current_weather']['temperature']

        response = {
            "hostname": socket.gethostname(),
            "datetime": datetime.utcnow().strftime("%y%m%d%H%M"),
            "version": VERSION,
            "message": "Hello from Dev!",
            "weather": {
                "dhaka": {
                    "temperature": str(temperature),
                    "temp_unit": "c"
                }
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        r = requests.get(WEATHER_API, timeout=5)
        if r.status_code == 200:
            return jsonify({"status": "healthy"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 503
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

