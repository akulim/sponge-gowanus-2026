import os
import pandas as pd
import math
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

# MODE 1: THE HISTORIAN (Oct 30 Data)
@app.route('/api/historical')
def get_historical():
    df = pd.read_csv('continuous (1).csv')
    df['time'] = pd.to_datetime(df['time'])
    # Filter for the Oct 30 surge you found
    storm = df[(df['time'] >= '2025-10-30') & (df['time'] <= '2025-10-31')].sort_values('time')
    return jsonify({
        "labels": storm['time'].dt.strftime('%H:%M').tolist(),
        "values": storm['value'].tolist()
    })

# MODE 2: THE ORACLE (March Forecast)
@app.route('/api/forecast')
def get_forecast():
    forecast = []
    start_date = datetime(2026, 3, 1, 0, 0)
    
    for i in range(48): # 48 hour forecast
        current_time = start_date + timedelta(hours=i)
        
        # TIDE MATH: High tide every 12.4 hours
        # We simulate the 0.5ft to 4.0ft range seen in your CSV
        tide = 1.0 + math.sin(i * (2 * math.pi / 12.4)) * 1.5
        
        # WEATHER PREDICTION: Add a "predicted" storm surge on March 2nd
        surge = 0
        if 24 <= i <= 36:
            surge = 2.0 # The "predicted" rain impact
            
        val = round(tide + surge, 2)
        forecast.append({"time": current_time.strftime('%b %d, %H:%M'), "value": val})
        
    return jsonify(forecast)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
