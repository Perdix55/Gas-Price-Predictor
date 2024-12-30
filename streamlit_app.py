import streamlit as st  
import pandas as pd  
import feedparser  
import re  
import matplotlib.pyplot as plt  

def fetch_gas_prices(url):  
    feed = feedparser.parse(url)  
    data = []  
    for entry in feed.entries:  
        try:  
            match = re.search(r'\$(\d+(\.\d+)?)', entry.summary)  
            if match:  
                price = float(match.group(1))  
                data.append({'date': entry.updated, 'price': price})  
        except Exception as e:  
            print(f"Error processing entry: {e}")  
    if not data:  
        return pd.DataFrame(columns=['date', 'price'])  
    return pd.DataFrame(data)  

def plot_trends(df):  
    df['date'] = pd.to_datetime(df['date'])  
    df = df.sort_values('date')  
    plt.plot(df['date'], df['price'], marker='o')  
    plt.title('Gas Price Trends')  
    plt.xlabel('Date')  
    plt.ylabel('Price (USD)')  
    plt.grid(True)  
    plt.show()  

rss_url = "https://www.eia.gov/petroleum/gasdiesel/includes/gas_diesel_rss.xml"  
gas_prices = fetch_gas_prices(rss_url)  

if gas_prices.empty:  
    st.write("No data available to plot.")  
else:  
    plot_trends(gas_prices)  
