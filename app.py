from flask import Flask, render_template, request, jsonify
import csv
import os
from model_logic import predict_from_keystrokes

# 1. INITIALIZE THE APP (This was likely missing or misspelled)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect')
def collect_page():
    return render_template('collect.html')

@app.route('/save_to_csv', methods=['POST'])
def save_to_csv():
    payload = request.json
    emotion = payload['emotion']
    data_list = payload['data']
    file_path = f'dataset/{emotion}.csv'
    
    os.makedirs('dataset', exist_ok=True)
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['key', 'hold_time', 'flight_time', 'latency', 'emotion'])
        for row in data_list:
            writer.writerow([row['key'], row['hold_time'], row['flight_time'], row['latency'], emotion])
            
    return jsonify({"message": f"Successfully saved to {emotion}.csv!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['timings']
        # Check if model exists before predicting
        if not os.path.exists('models/emotion_lstm.h5'):
            return jsonify({'emotion': 'Model not trained yet!'})
        
        emotion = predict_from_keystrokes(data)
        return jsonify({'emotion': emotion})
    except Exception as e:
        return jsonify({'emotion': f'Error: {str(e)}'})

# 2. RUN THE APP
if __name__ == '__main__':
    # Setting use_reloader=False can sometimes help prevent startup crashes in some IDEs
    app.run(debug=True, port=5000)