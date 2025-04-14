import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

# LSTM
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# For Keras Tuner (install via pip install keras-tuner)
import keras_tuner as kt

# XGBoost (commented out for now)
# import xgboost as xgb

# FastAPI
from fastapi import FastAPI
import uvicorn

#########################################
# STEP 1: Data Collection
#########################################
def fetch_data(symbol="AAPL", start="2000-01-01", end=None):
    if end is None:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    df = yf.download(symbol, start=start, end=end, interval="1d", auto_adjust=False)
    print(df.tail(5))
    df.dropna(inplace=True)
    if df.empty:
        raise ValueError(f"No data returned for {symbol} from {start} to {end}.")
    return df

#########################################
# STEP 2: Advanced Feature Engineering
#########################################
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # Avoid division by zero:
    avg_loss = avg_loss.replace(0, 1e-10)  # or add a small epsilon
    rs = avg_gain / avg_loss
    
    rsi = 100 - (100 / (1 + rs))
    return rsi


def add_technical_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['RSI_14'] = compute_rsi(df['Close'], 14)
    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    df['BB_std'] = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (2 * df['BB_std'])
    df['BB_lower'] = df['BB_middle'] - (2 * df['BB_std'])
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    low_min = df['Low'].rolling(window=14).min()
    high_max = df['High'].rolling(window=14).max()
    df['Stoch'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    # On Balance Volume (OBV)
    df['OBV'] = (np.where(df['Close'] > df['Close'].shift(1), df['Volume'],
                          np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0))
                 ).cumsum()
    df.dropna(inplace=True)
    return df

#########################################
# STEP 3: Data Preparation
#########################################
def prepare_data(df, drop_last=True):
    df['Target'] = df['Close'].shift(-1)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    if drop_last:
        df.dropna(inplace=True)
    else:
        # Only drop rows where feature columns (all columns except 'Target') have NaNs
        df.dropna(subset=[col for col in df.columns if col != 'Target'], inplace=True)
    print("After final dropna:", df.shape)
    return df


def load_and_prepare_for_prediction(symbol="AAPL", start="2000-01-01"):
    df = fetch_data(symbol, start)
    if df.empty:
        raise ValueError("No data returned from fetch_data.")
    df = add_technical_indicators(df)
    # Keep the latest row even if the target is missing.
    df = prepare_data(df, drop_last=False)
    if df.empty:
        raise ValueError("All rows dropped after feature engineering.")
    return df


# Define the feature set
features = ['Close', 'SMA_10', 'BB_upper', 'BB_lower', 
            'MACD', 'Signal_line', 'Stoch', 'Volume', 'OBV']

def load_and_prepare(symbol="AAPL", start="2000-01-01"):
    df = fetch_data(symbol, start)
    if df.empty:
        raise ValueError("No data was returned from fetch_data.")
    df = add_technical_indicators(df)
    df = prepare_data(df)
    if df.empty:
        raise ValueError("All rows dropped after feature engineering + target shift.")
    return df

#########################################
# Helper: Create Sequences for Time Series
#########################################
def create_sequences(features_array, targets, seq_length):
    X, y = [], []
    for i in range(len(features_array) - seq_length):
        X.append(features_array[i: i + seq_length])
        y.append(targets[i + seq_length])
    return np.array(X), np.array(y)

#########################################
# Keras Tuner Build Model Function
#########################################
def build_model(hp, input_shape):
    # Choose architecture: 'lstm', 'gru', or 'cnn_lstm'
    arch = hp.Choice('architecture', ['lstm', 'gru', 'cnn_lstm'])
    num_units = hp.Int('num_units', min_value=32, max_value=256, step=32)
    dropout_rate = hp.Float('dropout_rate', min_value=0.0, max_value=0.3, step=0.1)
    learning_rate = hp.Choice('learning_rate', [3e-4, 1e-4, 5e-5])
    
    model = keras.Sequential()
    if arch == 'lstm':
        model.add(layers.LSTM(num_units, return_sequences=True, input_shape=input_shape))
        model.add(layers.Dropout(dropout_rate))
        model.add(layers.LSTM(num_units))
        model.add(layers.Dropout(dropout_rate))
    elif arch == 'gru':
        model.add(layers.GRU(num_units, return_sequences=True, input_shape=input_shape))
        model.add(layers.Dropout(dropout_rate))
        model.add(layers.GRU(num_units))
        model.add(layers.Dropout(dropout_rate))
    elif arch == 'cnn_lstm':
        model.add(layers.Conv1D(filters=hp.Int('filters', min_value=16, max_value=64, step=16),
                                kernel_size=3,
                                activation='relu',
                                input_shape=input_shape))
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Dropout(dropout_rate))
        model.add(layers.LSTM(num_units))
        model.add(layers.Dropout(dropout_rate))
        
    model.add(layers.Dense(1))
    # Add gradient clipping to help stabilize training
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate, clipnorm=1.0)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

#########################################
# Full AutoML Approach: Tune over Sequence Lengths & Hyperparameters
#########################################
def full_auto_ml_approach(data_features, data_target, possible_seq_lengths=[30, 60, 90]):
    best_overall_mse = float('inf')
    best_overall_model = None
    best_overall_seq_len = None

    for seq_len in possible_seq_lengths:
        print(f"\n=== Testing sequence length = {seq_len} ===")
        X_seq, y_seq = create_sequences(data_features, data_target, seq_len)
        
        def model_builder(hp):
            return build_model(hp, input_shape=(seq_len, data_features.shape[1]))
        
        tuner = kt.RandomSearch(
            model_builder,
            objective='val_loss',
            max_trials=5,           # Increase for a more thorough search
            executions_per_trial=1,
            overwrite=True,
            directory='kt_dir',
            project_name=f"seq_len_{seq_len}"
        )
        tuner.oracle.max_consecutive_failed_trials = 10
        
        # Use a simple 80/20 split for tuning
        split_point = int(0.8 * len(X_seq))
        X_train, X_val = X_seq[:split_point], X_seq[split_point:]
        y_train, y_val = y_seq[:split_point], y_seq[split_point:]
        
        tuner.search(X_train, y_train,
                     validation_data=(X_val, y_val),
                     epochs=10,
                     batch_size=32,
                     verbose=1)
        
        best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]
        best_model = tuner.hypermodel.build(best_hp)
        preds_val = best_model.predict(X_val)
        mse_val = mean_squared_error(y_val, preds_val)
        print(f"Best model for seq_len={seq_len} has validation MSE: {mse_val:.4f}")
        
        if mse_val < best_overall_mse:
            best_overall_mse = mse_val
            best_overall_model = best_model
            best_overall_seq_len = seq_len

    print(f"\n=== Overall Best ===")
    print(f"Sequence length: {best_overall_seq_len}, MSE: {best_overall_mse:.4f}")
    return best_overall_model, best_overall_seq_len

#########################################
# Main Training Routine with AutoML (LSTM-Only)
#########################################
def auto_ml_train_models(symbol="AAPL", start="2000-01-01", possible_seq_lengths=[30, 60, 90], test_ratio=0.2):
    df = load_and_prepare(symbol, start)
    
    # Scale features and target
    scaler_features = MinMaxScaler()
    scaler_target = MinMaxScaler()
    data_features = scaler_features.fit_transform(df[features])
    data_target = scaler_target.fit_transform(df[['Target']]).flatten()
    
    # Use AutoML approach to select best model & sequence length
    best_model, best_seq_len = full_auto_ml_approach(data_features, data_target, possible_seq_lengths)
    
    # Create sequences with best sequence length and split into train/test sets
    X_seq, y_seq = create_sequences(data_features, data_target, best_seq_len)
    total_sequences = len(df) - best_seq_len
    split_index = int(total_sequences * (1 - test_ratio))
    X_train_seq, X_test_seq = X_seq[:split_index], X_seq[split_index:]
    y_train_seq, y_test_seq = y_seq[:split_index], y_seq[split_index:]
    
    # Optionally, retrain the best_model on the entire training set
    best_model.fit(X_train_seq, y_train_seq,
                   epochs=10,
                   batch_size=32,
                   validation_split=0.1,
                   verbose=1)
    
    # Evaluate on test set
    preds_test = best_model.predict(X_test_seq)
    y_test_actual = scaler_target.inverse_transform(y_test_seq.reshape(-1, 1))
    preds_actual = scaler_target.inverse_transform(preds_test)
    
    print("\nLSTM-Only AutoML Performance on Test Set:")
    mse_val, rmse_val, mae_val = evaluate_model_performance(y_test_actual.flatten(), preds_actual.flatten())
    print(f"Test MSE: {mse_val:.4f}, RMSE: {rmse_val:.4f}, MAE: {mae_val:.4f}")
    
    # Backtesting using the test predictions
    test_start_index = split_index + best_seq_len
    final_value = backtest_strategy(df, preds_test.flatten(), test_start_index)
    print(f"Backtested portfolio final value: {final_value}")
    
    return best_model, best_seq_len, scaler_features, scaler_target, df

#########################################
# Model Evaluation Helper Function
#########################################
def evaluate_model_performance(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_true - y_pred))
    
    print("Evaluation Metrics:")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    
    plt.figure(figsize=(12,6))
    plt.plot(y_true, label="Actual Prices", marker='o')
    plt.plot(y_pred, label="Predicted Prices", marker='x')
    plt.title("Predicted vs Actual Prices on Test Set")
    plt.xlabel("Time Step")
    plt.ylabel("Price")
    plt.legend()
    plt.show()
    
    return mse, rmse, mae

#########################################
# Backtesting Helper Function
#########################################
def backtest_strategy(df, predictions, test_start, transaction_cost=0.001, slippage=0.001):
    df_backtest = df.iloc[test_start:].copy().reset_index(drop=True)
    min_len = min(len(df_backtest), len(predictions))
    df_backtest = df_backtest.iloc[:min_len]
    predictions = predictions[:min_len]
    
    df_backtest['Prediction'] = np.array(predictions).ravel()
    df_backtest['ShiftedClose'] = df_backtest['Close'].shift(1)
    df_backtest['Signal'] = (df_backtest['Prediction'] > df_backtest['ShiftedClose']).astype(bool)
    
    capital = 10000.0
    position = 0.0
    cash = capital

    for i, signal in enumerate(df_backtest['Signal']):
        row = df_backtest.iloc[i]
        if signal and cash > 0:
            buy_price = row['Close'] * (1 + slippage)
            position = (cash * (1 - transaction_cost)) / buy_price
            cash = 0
        elif (not signal) and position > 0:
            sell_price = row['Close'] * (1 - slippage)
            cash = position * sell_price * (1 - transaction_cost)
            position = 0

    final_price = df_backtest.iloc[-1]['Close'] * (1 - slippage)
    final_value = cash + (position * final_price if position > 0 else 0)
    return final_value

#########################################
# Train and Evaluate using AutoML (LSTM-Only)
#########################################
lstm_model, best_seq_len, scaler_features, scaler_target, df_for_training = auto_ml_train_models(
    symbol="AAPL",
    start="2000-01-01",
    possible_seq_lengths=[30, 60, 90],
    test_ratio=0.2
)

#########################################
# FastAPI for Real-Time Prediction (LSTM-Only)
#########################################
app = FastAPI()

@app.get("/predict")
def predict_next_day(symbol: str = "AAPL"):
    df_latest = load_and_prepare_for_prediction(symbol, start="2000-01-01")
    print(f"Latest data for {symbol}: {df_latest.tail(5)}")
    # Use the best sequence length from AutoML for the prediction window
    bigger_slice = df_latest.tail(best_seq_len+1)
    df_window = bigger_slice.iloc[1:]
    last_date = df_window.index[-1]

    data_latest = scaler_features.transform(df_window[features])
    latest_sequence = np.expand_dims(data_latest, axis=0)

    # Use only the LSTM model for prediction
    lstm_pred_scaled = lstm_model.predict(latest_sequence)[0, 0]
    pred_price = scaler_target.inverse_transform([[lstm_pred_scaled]])[0, 0]
    
    predicted_date = last_date + pd.Timedelta(days=1)
    
    return {
        "inference_date": str(last_date.date()),
        "predicted_date": str(predicted_date.date()),
        "predicted_price": round(float(pred_price), 2)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#documentation

"""
Adaptive Stock Prediction System
==================================

This module implements an adaptive stock prediction system using an ensemble approach that 
combines LSTM (Long Short-Term Memory) networks and XGBoost models. It is designed to address 
the unpredictability of financial markets by integrating several advanced strategies:

1. Uncertainty Quantification
   -----------------------------
   - **Monte Carlo Dropout:**  
     During inference, dropout is enabled to simulate an ensemble of models. Multiple 
     forward passes are executed to obtain a distribution of predictions. The mean and 
     variance of these predictions provide an estimate of prediction uncertainty.
     
   - **Ensemble Variance:**  
     When maintaining multiple models (or retraining periodically), the variance across 
     ensemble predictions can be measured. High variance indicates unstable market conditions.

2. Online Learning and Continuous Retraining
   --------------------------------------------
   - **Periodic Retraining:**  
     Markets evolve over time. The `retrain_model` function reloads and preprocesses the 
     latest market data, then retrains (or fine-tunes) the models. This can be scheduled 
     to run daily or weekly or triggered by significant performance drops, reducing model 
     drift over time.
     
   - **Adaptive Learning Rates:**  
     By using adaptive learning rate techniques (or tools such as Keras Tuner), the LSTM 
     model can adjust its learning rate based on recent performance, thereby better adapting 
     to new market patterns.

3. Adaptive Ensemble Methods
   ---------------------------
   - **Weighted Averaging:**  
     Instead of a simple average of the LSTM and XGBoost predictions, the system uses a 
     weighted average. Weights are assigned based on the recent performance of each model. 
     For instance, if the LSTM model has demonstrated higher accuracy recently, it can be 
     given a higher weight.
     
   - **Model Monitoring:**  
     A monitoring framework should be implemented to continuously track model performance. 
     If one model underperforms or if overall prediction uncertainty increases, the system 
     can trigger a retraining cycle or adjust ensemble weights dynamically.

4. Incorporating Additional Data Sources
   ----------------------------------------
   - **Exogenous Variables:**  
     The model’s feature set can be extended to include external data such as news sentiment, 
     economic indicators (interest rates, GDP growth, etc.), and social media trends. This extra 
     information helps capture market influences that historical price data alone might miss.
     
   - **Market Regime Indicators:**  
     Using technical indicators or clustering techniques, the system can identify different 
     market regimes (e.g., trending vs. mean-reverting). Once detected, the strategy or ensemble 
     weights can be adjusted to better suit the current market condition.

Usage:
------
- **Uncertainty Quantification:**  
  Use `mc_dropout_prediction(model, input_data, n_iter)` to get the mean prediction and its 
  uncertainty from the LSTM model.
  
- **Online Learning:**  
  Call `retrain_model(symbol, start_date, seq_length)` periodically to update and retrain 
  the models with the latest market data.
  
- **Adaptive Ensemble Prediction:**  
  Use `weighted_ensemble_predict(lstm_model, xgb_model, scaler_target, latest_sequence, latest_tab, weight_lstm, weight_xgb)` 
  to obtain a weighted prediction based on the recent performance of each model.

Note:
-----
While this system incorporates advanced techniques to handle market unpredictability, no 
model can entirely eliminate the risks associated with financial forecasting. Continuous 
monitoring, risk management, and further enhancements (e.g., incorporating additional data 
sources) are recommended for production-level deployment.

Future Extensions:
------------------
- Integration of external data sources such as sentiment analysis or macroeconomic indicators.
- Implementation of advanced risk management metrics (e.g., drawdown, Sharpe ratio, stop-loss/take-profit rules).
- Automation of model monitoring and dynamic weight adjustments based on performance.

Author: [Your Name]
Date: [Current Date]
"""
