import pandas as pd
import yfinance as yf
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

def fetch_trading_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def update_google_sheet(sheet_id, range_name, values):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets'])
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)

    sheet_id = config['sheet_id']
    symbols = config['symbols']
    start_date = config['start_date']
    end_date = config['end_date']

    all_data = []
    for symbol in symbols:
        data = fetch_trading_data(symbol, start_date, end_date)
        if data is not None:
            data['Symbol'] = symbol
            all_data.append(data)

    if all_data:
        combined_data = pd.concat(all_data)
        combined_data.reset_index(inplace=True)
        values = [combined_data.columns.tolist()] + combined_data.values.tolist()
        update_google_sheet(sheet_id, 'A1', values)
    else:
        print("No data fetched. Check your symbols and date range.")

if __name__ == "__main__":
    main()