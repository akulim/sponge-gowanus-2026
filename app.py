from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('gowanus_full_data.csv', parse_dates=['time'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Get date from request, or default to latest
    target_date = request.args.get('date', '2026-02-21')
    
    # Filter for a 24-hour window around that date
    mask = (df['time'] >= target_date) & (df['time'] <= pd.to_datetime(target_date) + pd.Timedelta(days=1))
    slice_df = df.loc[mask]
    
    return jsonify({
        "labels": slice_df['time'].dt.strftime('%H:%M').tolist(),
        "levels": slice_df['water_level'].tolist(),
        "toxins": slice_df['contamination'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
