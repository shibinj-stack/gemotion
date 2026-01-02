import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
import pickle
import os
from preprocess import prepare_lstm_data

def run_training():
    data = prepare_lstm_data(window_size=10)
    if data is None: return
    
    (X_train, X_test, y_train, y_test), label_encoder = data
    
    model = Sequential([
        Input(shape=(10, 3)),
        LSTM(32, return_sequences=True), # Reduced units to prevent overfitting on small data
        Dropout(0.3),
        LSTM(16),
        Dropout(0.3),
        Dense(16, activation='relu'),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])

    # Early Stopping: Stops training when validation loss stops improving
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True
    )

    print("Starting optimized training...")
    model.fit(
        X_train, y_train, 
        epochs=100, # Increased max epochs, EarlyStopping will handle the rest
        validation_data=(X_test, y_test), 
        batch_size=16,
        callbacks=[early_stop]
    )

    os.makedirs('models', exist_ok=True)
    model.save('models/emotion_lstm.h5')
    with open('models/classes.pkl', 'wb') as f:
        pickle.dump(label_encoder.classes_, f)
    
    print("Optimized Model and Scaler saved.")

if __name__ == "__main__":
    run_training()