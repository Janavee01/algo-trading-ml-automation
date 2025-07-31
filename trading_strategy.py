import pandas as pd
import ta
import matplotlib.pyplot as plt
import os

# === CONFIG ===
stock_symbols = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS']
col_names = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
data_folder = 'stock_data'

# === PROCESS EACH STOCK ===
for symbol in stock_symbols:
    file_path = os.path.join(data_folder, f"{symbol}_data.csv")
    print(f"\n📈 Processing {symbol}...")

    try:
        # Load CSV, skip metadata, name columns
        df = pd.read_csv(file_path, skiprows=3, names=col_names)

        # Clean index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # Calculate indicators
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        df['20DMA'] = df['Close'].rolling(window=20).mean()
        df['50DMA'] = df['Close'].rolling(window=50).mean()

        # Buy signal condition
        df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
        df.dropna(subset=['RSI', '20DMA', '50DMA'], inplace=True)

        # Show Buy Signals
        buy_signals = df[df['Buy_Signal']]
        print(f"📌 {len(buy_signals)} Buy Signals for {symbol}")
        if not buy_signals.empty:
            print(buy_signals[['Close', 'RSI', '20DMA', '50DMA']])

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(df['Close'], label='Close Price', alpha=0.6)
        plt.plot(df['20DMA'], label='20DMA', linestyle='--', color='orange')
        plt.plot(df['50DMA'], label='50DMA', linestyle='--', color='green')
        plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', s=100)
        plt.title(f'{symbol} Buy Signals (RSI < 30 & 20DMA > 50DMA)')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")
