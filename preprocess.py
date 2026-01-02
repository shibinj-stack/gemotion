import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def prepare_lstm_data(data_dir='dataset', window_size=10):
    all_data = []
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} folder not found.")
        return None
        
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            path = os.path.join(data_dir, filename)
            df = pd.read_csv(path)
            all_data.append(df)
    
    if not all_data:
        return None

    full_df = pd.concat(all_data, ignore_index=True)
    
    # Feature Scaling: Vital for LSTMs to converge properly
    features = ['hold_time', 'flight_time', 'latency']
    scaler = StandardScaler()
    full_df[features] = scaler.fit_transform(full_df[features])
    
    # Save scaler to use during prediction
    os.makedirs('models', exist_ok=True)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    encoder = LabelEncoder()
    full_df['emotion'] = encoder.fit_transform(full_df['emotion'])
    
    X, y = [], []
    for emotion_code in full_df['emotion'].unique():
        emotion_df = full_df[full_df['emotion'] == emotion_code]
        feature_values = emotion_df[features].values
        
        for i in range(len(feature_values) - window_size + 1):
            X.append(feature_values[i : i + window_size])
            y.append(emotion_code)
            
    X = np.array(X) 
    y = np.array(y)
    
    return train_test_split(X, y, test_size=0.2, random_state=42), encoder