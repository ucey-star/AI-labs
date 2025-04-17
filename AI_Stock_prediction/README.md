# 📈 Adaptive Stock Price Prediction with LSTM & AutoML

This project builds a **real-time stock price prediction system** using LSTM neural networks and AutoML techniques. It features a complete pipeline—from data collection to model training and deployment using **FastAPI** for live predictions.

---

## 🔧 Key Features

- 📊 **Advanced Technical Indicators**: RSI, MACD, Bollinger Bands, OBV, and more
- 🤖 **LSTM Neural Network**: For time-series modeling
- ⚙️ **AutoML with Keras Tuner**: Automatically finds optimal model hyperparameters and sequence lengths
- 📈 **Backtesting Engine**: Simulates a simple buy/sell strategy using predictions
- 🚀 **FastAPI Endpoint**: Real-time prediction with HTTP request support
- 📉 **Evaluation Metrics**: MSE, RMSE, MAE, plus visual plots

---

## 🛠️ Tech Stack

- Python 3  
- yFinance (for data)  
- NumPy, Pandas, Matplotlib  
- Scikit-learn (scaling + metrics)  
- TensorFlow/Keras (LSTM model)  
- Keras Tuner (AutoML)  
- FastAPI + Uvicorn (API server)

---

## 📦 Installation

Install the required packages:

```bash
pip install yfinance numpy pandas matplotlib scikit-learn tensorflow keras keras-tuner fastapi uvicorn
```

---

## 🚀 How It Works

### ✅ 1. **Data Collection & Feature Engineering**
- Fetches daily stock data using `yfinance`
- Adds technical indicators like RSI, MACD, Bollinger Bands, OBV

### ✅ 2. **Data Preparation**
- Targets are defined as the next day’s closing price
- Features are normalized using MinMaxScaler
- Time-series sequences are created for LSTM input

### ✅ 3. **Model Training (AutoML)**
- Tries multiple architectures: `LSTM`, `GRU`, `CNN-LSTM`
- Tunes hyperparameters like units, dropout, learning rate
- Finds the best sequence length and architecture automatically

### ✅ 4. **Model Evaluation**
- Plots predicted vs actual values
- Calculates MSE, RMSE, and MAE

### ✅ 5. **Backtesting**
- Simulates a basic long-only strategy
- Reports final portfolio value based on predictions

### ✅ 6. **Real-Time API**
- Hosted via FastAPI
- Endpoint: `/predict?symbol=AAPL`

Example:

```bash
curl "http://localhost:8000/predict?symbol=TSLA"
```

---

## 🧪 Example Output

```
{
  "inference_date": "2024-04-16",
  "predicted_date": "2024-04-17",
  "predicted_price": 181.27
}
```

---

## 📈 Evaluation Example

```
Test MSE: 2.1517
Test RMSE: 1.4660
Test MAE: 1.1215
```

![Evaluation Plot](#)

---

## 📊 Backtesting

The backtesting engine uses predictions to simulate trades. When the predicted next-day price is higher than today’s, the model buys. Otherwise, it holds/sells.

```
Backtested portfolio final value: $13,452.73 (starting from $10,000)
```

---

## 🔮 Future Extensions

- Incorporate **news sentiment**, **economic data**, or **social media trends**
- Implement **uncertainty quantification** (e.g., Monte Carlo Dropout)
- Add **XGBoost**, **ensemble methods**, or **adaptive weighting**
- Use **regime detection** to change strategies based on market condition

---

## 📡 Running the API

```bash
uvicorn your_script:app --host 0.0.0.0 --port 8000
```

---

## 📁 Project Structure

```
.
├── stock_predictor.py       # Core model and training logic
├── indicators.py            # Feature engineering
├── api.py                   # FastAPI endpoint
├── README.md
```

---

## 📝 License

This project is open-source and intended for educational and research use. It is **not** financial advice.

---