import os
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/historical')
def get_historical():
    print("API: Historical request received")
    try:
        # Check if file exists first
        if not os.path.exists('continuous (1).csv'):
            print("ERROR: continuous.csv NOT FOUND in root directory")
            return jsonify({"error": "File not found"}), 404
            
        # Read file
        df = pd.read_csv('continuous (1).csv')
        print(f"SUCCESS: Loaded CSV with {len(df)} rows")
        print(f"COLUMNS FOUND: {df.columns.tolist()}")

        df['time'] = pd.to_datetime(df['time'])
        
        # Grab the biggest spike to ensure we have data
        storm = df.sort_values('value', ascending=False).head(100).sort_values('time')
        
        data = {
            "labels": storm['time'].dt.strftime('%m/%d %H:%M').tolist(),
            "values": storm['value'].tolist()
        }
        print(f"SENDING: {len(data['values'])} data points")
        return jsonify(data)
        
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/forecast')
def get_forecast():
    import math
    from datetime import datetime, timedelta
    print("API: Forecast request received")
    forecast = []
    start = datetime(2026, 3, 1)
    for i in range(48):
        tide = 1.0 + math.sin(i * (2 * math.pi / 12.4)) * 1.5
        val = round(tide + (2.0 if 24 <= i <= 36 else 0), 2)
        forecast.append({"time": (start + timedelta(hours=i)).strftime('%H:%M'), "value": val})
    return jsonify(forecast)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
