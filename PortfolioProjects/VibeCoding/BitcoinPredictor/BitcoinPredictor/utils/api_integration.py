import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import time

def fetch_bitcoin_price_coingecko():
    """Fetch current Bitcoin price from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'bitcoin' in data:
            btc_data = data['bitcoin']
            return {
                'price': btc_data.get('usd', 0),
                'change_24h': btc_data.get('usd_24h_change', 0),
                'volume_24h': btc_data.get('usd_24h_vol', 0),
                'last_updated': btc_data.get('last_updated_at', int(time.time()))
            }
        
        return None
        
    except Exception as e:
        st.error(f"Error fetching Bitcoin price: {str(e)}")
        return None

def fetch_bitcoin_historical_coingecko(days=365):
    """Fetch historical Bitcoin price data from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract prices and volumes
        prices = data.get('prices', [])
        volumes = data.get('total_volumes', [])
        
        # Create DataFrame
        df_data = []
        for i, (timestamp, price) in enumerate(prices):
            date = datetime.fromtimestamp(timestamp / 1000)
            volume = volumes[i][1] if i < len(volumes) else 0
            
            df_data.append({
                'Date': date,
                'Open': price,  # CoinGecko doesn't provide OHLC for free, using price as approximation
                'High': price * 1.01,  # Approximate high
                'Low': price * 0.99,   # Approximate low
                'Close': price,
                'Adj Close': price,
                'Volume': volume
            })
        
        df = pd.DataFrame(df_data)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching historical Bitcoin data: {str(e)}")
        return None

def update_data_with_latest_price(existing_data):
    """Update existing data with the latest Bitcoin price"""
    try:
        current_price_data = fetch_bitcoin_price_coingecko()
        
        if current_price_data is None:
            return existing_data
        
        # Get the last date in existing data
        last_date = existing_data['Date'].max()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # If last date is not today, add new rows
        if last_date.date() < today.date():
            days_to_add = (today - last_date).days
            
            # Fetch recent historical data to fill the gap
            recent_data = fetch_bitcoin_historical_coingecko(days=days_to_add + 1)
            
            if recent_data is not None:
                # Filter only new dates
                recent_data = recent_data[recent_data['Date'] > last_date]
                
                if len(recent_data) > 0:
                    # Combine with existing data
                    updated_data = pd.concat([existing_data, recent_data], ignore_index=True)
                    updated_data = updated_data.sort_values('Date').reset_index(drop=True)
                    return updated_data
        
        return existing_data
        
    except Exception as e:
        st.error(f"Error updating data: {str(e)}")
        return existing_data

def get_live_bitcoin_metrics():
    """Get live Bitcoin metrics for dashboard display"""
    try:
        price_data = fetch_bitcoin_price_coingecko()
        
        if price_data:
            return {
                'current_price': price_data['price'],
                'change_24h': price_data['change_24h'],
                'volume_24h': price_data['volume_24h'],
                'last_updated': datetime.fromtimestamp(price_data['last_updated']).strftime('%Y-%m-%d %H:%M:%S')
            }
        
        return None
        
    except Exception as e:
        st.error(f"Error getting live metrics: {str(e)}")
        return None
