import yfinance as yf
import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import NamedStyle  # Import NamedStyle for formatting
import subprocess
import platform

ALPHA_VANTAGE_API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# Step 1: Retrieve historical stock data using Yahoo Finance
def get_historical_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Step 2: Retrieve earnings data using the Alpha Vantage API
def get_eps_data(ticker):
    base_url = f'https://www.alphavantage.co/query'
    function = 'EARNINGS'
    symbol = ticker
    api_key = ALPHA_VANTAGE_API_KEY

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'quarterlyEarnings' in data:
        eps_data = pd.DataFrame(data['quarterlyEarnings'])
        return eps_data
    else:
        raise Exception(f"Error retrieving earnings data: {data}")

# Step 3: Save data to an Excel file
def save_to_excel(historical_data, eps_data, ticker):
    workbook = Workbook()

    # Create a custom style for formatting dates
    date_style = NamedStyle(name='date_style', number_format='YYYY-MM-DD')

    historical_sheet = workbook.active
    historical_sheet.title = 'HistoricalData'

    # Add headers for historical data
    historical_sheet.append(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    # Apply the date style to the first row
    for cell in historical_sheet['1:1']:
        cell.style = date_style

    # Populate historical data
    for row in dataframe_to_rows(historical_data, index=True, header=False):
        historical_sheet.append(row)

    eps_sheet = workbook.create_sheet(title='EPSData')

    # Add headers for EPS data
    eps_sheet.append(['Reported Date', 'Fiscal Date Ending', 'EPS Surprise (%)', 'Reported EPS', 'Estimated EPS'])

    file_path = f'{ticker}_data.xlsx'

    # Apply the date style to the first row
    for cell in eps_sheet['1:1']:
        cell.style = date_style

    # Populate EPS data
    for row in dataframe_to_rows(eps_data, index=False, header=False):
        eps_sheet.append(row)

    # Save the Excel file
    workbook.save(file_path)
    return file_path

# Step 4: Open Excel file using the default application
def open_excel(file_path):
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(['start', 'excel', file_path], shell=True)
    elif system == 'Linux':
        subprocess.Popen(['xdg-open', file_path])
    elif system == 'Darwin':  # macOS
        subprocess.Popen(['open', file_path])
    else:
        print(f"Unsupported operating system: {system}")

# Step 5: Main program
def main():
    print("Welcome to the Stock Data Retrieval Program!")
    ticker = input("Enter the stock ticker symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    try:
        # Retrieve historical stock data
        historical_data = get_historical_data(ticker, start_date, end_date)

        # Retrieve earnings data
        eps_data = get_eps_data(ticker)

        # Save data to Excel file
        file_path = save_to_excel(historical_data, eps_data, ticker)
        print(f"\nData has been saved to {file_path}. Opening Excel file...")

        # Open the Excel file using the default application
        open_excel(file_path)
    except Exception as e:
        print(f"Error retrieving data: {e}")

# Step 6: Execute the main program
if __name__ == "__main__":
    main()
