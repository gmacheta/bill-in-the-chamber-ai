from scrape import fetch_legislation_data
from ai_analysis import analyze_text_with_model

def test_integration(query):
    """Test the integration of fetching and analyzing Congress data."""
    try:
        # Fetch data from Congress.gov
        data = fetch_legislation_data(query)
        
        # Analyze data to get focus areas
        focus_areas = analyze_text_with_model(data)
        
        return focus_areas
    except Exception as e:
        print(f"Error: {e}")

# Run the test
if __name__ == "__main__":
    print(test_integration("technology funding"))
