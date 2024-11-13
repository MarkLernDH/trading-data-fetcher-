# Trading Data Fetcher

This automation script fetches historical trading data for various symbols across exchanges and updates a Google Sheet with the collected data.

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up Google Sheets API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API
   - Create credentials (OAuth client ID)
   - Download the client configuration and save it as `credentials.json` in the project directory
4. Run the authorization flow:
   ```python
   from google_auth_oauthlib.flow import InstalledAppFlow

   flow = InstalledAppFlow.from_client_secrets_file(
       'credentials.json',
       ['https://www.googleapis.com/auth/spreadsheets']
   )
   creds = flow.run_local_server(port=0)
   with open('token.json', 'w') as token:
       token.write(creds.to_json())
   ```
5. Update the `config.json` file with your desired settings

## Configuration

Edit the `config.json` file to set your preferences:

```json
{
  "sheet_id": "your_google_sheet_id",
  "symbols": ["AAPL", "GOOGL", "MSFT"],
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

## Usage

Run the script:

```
python script.py
```

The script will fetch the trading data for the specified symbols and date range, then update the Google Sheet with the collected data.

## Note

Ensure that you have the necessary permissions to access and modify the Google Sheet specified in the configuration.