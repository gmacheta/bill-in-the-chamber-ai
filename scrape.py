import requests
from config.api_keys import CONGRESS_API_KEY


def fetch_legislation_data(query):
    """Fetch detailed bill data from Congress.gov API based on a search query."""
    url = f"https://api.congress.gov/v3/bill?query={query}&api_key={CONGRESS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        bills = data.get("bills", [])
        
        # Fetch additional details for each bill
        detailed_bills = []
        for bill in bills:
            try:
                bill_url = bill.get("url")
                bill_data = requests.get(bill_url).json()
                detailed_bills.append(bill_data)
            except Exception as e:
                print(f"Failed to fetch details for bill {bill.get('number')}: {e}")
        
        return detailed_bills
    except Exception as e:
        print(f"Failed to fetch data for query '{query}': {e}")
        return []
