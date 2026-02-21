from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data/<mode>')
def get_data(mode):
    file = 'before_data.csv' if mode == 'before' else 'after_data.csv'
    df = pd.read_csv(file)
    
    labels = df['time'].tolist()
    values = df['value'].tolist()
    
    # We judge the "Current Status" by the very last value in the list
    latest_val = values[-1]
    
    if mode == 'before':
        # "Before" mode is always "Unpredictable"
        status = {"color": "#6b7280", "msg": "MODE: RAW SENSOR", "act": "Data is unverified."}
    else:
        # "After" mode uses our Logic
        if latest_val < 1.6:
            status = {"color": "#10b981", "msg": "SAFE: Tidal Baseline", "act": "Kayaking Allowed"}
        elif latest_val < 2.3:
            status = {"color": "#f59e0b", "msg": "CAUTION: Rising Tide", "act": "Walking Only"}
        else:
            status = {"color": "#ef4444", "msg": "DANGER: Flood/CSO Alert", "act": "Stay Away - Contamination Risk"}

    return jsonify({"labels": labels, "values": values, "status": status, "current": round(latest_val, 2)})

if __name__ == '__main__':
    app.run(debug=True)
