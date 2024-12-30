import re
import pandas as pd
import feedparser

def fetch_gas_prices(url):
    feed = feedparser.parse(url)
    data = []  # Initialize the list
    if not feed.entries:
        print("No entries in RSS feed.")
        return pd.DataFrame(columns=['date', 'price'])  # Return an empty DataFrame
    for entry in feed.entries:
        try:
            match = re.search(r'\$(\d+(\.\d+)?)', entry.summary)
            if match:
                price = float(match.group(1))
                data.append({'date': entry.updated, 'price': price})
            else:
                print(f"Entry summary does not match expected format: {entry.summary}")
        except Exception as e:
            print(f"Error processing entry: {e}")
    if not data:
        print("No valid data found.")
        return pd.DataFrame(columns=['date', 'price'])
    return pd.DataFrame(data)


#Use Pandas and Matplotlib to visualize price trends

import matplotlib.pyplot as plt

def plot_trends(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    plt.plot(df['date'], df['price'], marker='o')
    plt.title('Gas Price Trends')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.show()

plot_trends(gas_prices)

#Use a simple regression model for prediction

from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_prices(df):
    df['date_numeric'] = (df['date'] - df['date'].min()).dt.days
    model = LinearRegression()
    X = np.array(df['date_numeric']).reshape(-1, 1)
    y = df['price']
    model.fit(X, y)
    future_days = np.array([df['date_numeric'].max() + i for i in range(1, 8)]).reshape(-1, 1)
    predictions = model.predict(future_days)
    return predictions

predictions = forecast_prices(gas_prices)

#Streamlit Front-End

import streamlit as st

st.title("Gas Price Forecasting App")
st.write("Check whether gas prices are increasing or decreasing based on historical data.")

st.subheader("Gas Price Trends")
st.line_chart(data=gas_prices.set_index('date')['price'])

st.subheader("Predicted Gas Prices for the Next Week")
for i, pred in enumerate(predictions, start=1):
    st.write(f"Day {i}: ${pred:.2f}")
