import os
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/historical')
def get_historical():
    try:
        # Load the file - standard comma now
        df = pd.read_csv('continuous (1).csv')
        df['time'] = pd.to_datetime(df['time'])
        
        # BROAD FILTER: Look for the big Oct 30 surge
        storm = df[(df['time'] >= '2025-10-30') & (df['time'] <= '2025-10-31')].sort_values('time')
        
        # BACKUP: If Oct 30 is empty, just grab the last 200 rows of the file
        if storm.empty:
            storm = df.sort_values('time').tail(200)
            
        return jsonify({
            "labels": storm['time'].dt.strftime('%m/%d %H:%M').tolist(),
            "values": storm['value'].tolist()
        })
    except Exception as e:
        print(f"Error reading CSV: {e}") # This will now show up in Render Logs
        return jsonify({"error": str(e)}), 500

@app.route('/api/forecast')
def get_forecast():
    # Use the same logic we had before for the March math
    import math
    from datetime import datetime, timedelta
    forecast = []
    start = datetime(2026, 3, 1)
    for i in range(48):
        tide = 1.0 + math.sin(i * (2 * math.pi / 12.4)) * 1.5
        val = round(tide + (2.0 if 24 <= i <= 36 else 0), 2)
        forecast.append({"time": (start + timedelta(hours=i)).strftime('%b %d, %H:%M'), "value": val})
    return jsonify(forecast)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
