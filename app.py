import os
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    event = request.args.get('event', 'current')
    
    # Historical Data Archive (Rain in mm)
    # 0mm = Clear, 50mm = Flood, 120mm = Extreme
    data_points = {
        'current': 0.5,
        'ida': 180,        # Hurricane Ida
        'cloudburst': 120, # Sept 2023 Flood
        'moderate': 35     # Typical Storm
    }
    
    rain = data_points.get(event, 0)
    
    # Logic for contamination and height
    # Height scales from 20% to 95%
    h_level = min(95, 20 + (rain * 0.6)) 
    
    # Safety Prediction
    if rain > 50:
        prediction = "DANGER: EXTREME FLOOD & SEWAGE"
        color = "#e74c3c" # Red
    elif rain > 5:
        prediction = "WARNING: CSO OVERFLOW ACTIVE"
        color = "#f1c40f" # Yellow
    else:
        prediction = "SAFE FOR RECREATION"
        color = "#2ecc71" # Green

    return jsonify({
        "rain": rain,
        "water_level": h_level,
        "prediction": prediction,
        "color": color
    })

if __name__ == "__main__":
    # This port logic is the key to fixing 502 errors
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
