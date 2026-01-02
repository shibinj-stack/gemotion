import numpy as np
import tensorflow as tf
import pickle
import os

MODEL = None
CLASSES = None
SCALER = None

def load_resources():
    global MODEL, CLASSES, SCALER
    if MODEL is None:
        MODEL = tf.keras.models.load_model('models/emotion_lstm.h5')
        with open('models/classes.pkl', 'rb') as f:
            CLASSES = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            SCALER = pickle.load(f)

def predict_from_keystrokes(raw_timings):
    load_resources()
    recent_data = raw_timings[-10:]
    
    features = []
    for k in recent_data:
        features.append([float(k['hold_time']), float(k['flight_time']), float(k['latency'])])
    
    # Scale the real-time data before prediction
    scaled_features = SCALER.transform(features)
    
    input_array = np.array(scaled_features).reshape(1, 10, 3)
    prediction = MODEL.predict(input_array)
    class_index = np.argmax(prediction)
    
    return CLASSES[class_index]