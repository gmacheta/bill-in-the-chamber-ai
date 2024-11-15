def build_political_profiles():
    """Build political profiles for each senator and representative."""
    # Example static data. Replace with real data fetching logic.
    return {
        "Senator A": {"party": "Democrat", "state": "CA", "ideology": "progressive"},
        "Senator B": {"party": "Republican", "state": "TX", "ideology": "conservative"},
    }

def predict_votes(profiles, bill_metadata):
    """Predict votes based on political profiles and bill metadata."""
    votes = {}
    for senator, profile in profiles.items():
        if "progressive" in bill_metadata.get("keywords", []) and profile["ideology"] == "progressive":
            votes[senator] = "Yes"
        else:
            votes[senator] = "No"
    return votes
