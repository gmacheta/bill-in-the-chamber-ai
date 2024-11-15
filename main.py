import modal
from scrape import fetch_legislation_data
from ai_analysis import analyze_bills
from profiles import build_political_profiles, predict_votes

# Updated image to include dependencies
image = modal.Image.debian_slim().pip_install(["requests", "transformers", "torch", "scikit-learn"])

app = modal.App(name="fundsight-ai", image=image)

@app.function()
def analyze_legislation(query="technology funding"):
    """Fetch and analyze legislation data."""
    # Step 1: Fetch data
    bills = fetch_legislation_data(query)
    if not bills:
        return {"error": f"No data fetched for query: {query}. Ensure the Congress API is returning valid results."}
    
    # Step 2: Analyze bills
    analyses = analyze_bills(bills)
    if not analyses:
        return {"error": "No meaningful analyses generated. Check Together AI setup and data quality."}
    
    # Step 3: Build profiles and predict votes
    profiles = build_political_profiles()
    predictions = []
    for analysis in analyses:
        bill_metadata = {"keywords": analysis.get("keywords", [])}
        votes = predict_votes(profiles, bill_metadata)
        predictions.append({"bill": analysis.get("bill", ""), "votes": votes})

    # Step 4: Output results
    results = {"analyses": analyses, "predictions": predictions}
    print("Analysis and predictions completed successfully.")
    return results

if __name__ == "__main__":
    analyze_legislation("technology funding")
