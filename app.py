import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/historical-data')
def get_historical():
    # Simulated data reflecting the Sept 2023 flood event
    # Hours represents a 12-hour window during a storm
    data = {
        "labels": ["12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"],
        "precipitation": [0, 2, 15, 45, 80, 40, 10, 5], # mm
        "contamination": [150, 400, 2500, 8000, 15000, 12000, 9000, 6000] # CFU/100mL
    }
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
