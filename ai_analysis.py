import requests
from transformers import pipeline

# Replace with your own API key for Together AI or any external service
TOGETHER_API_KEY = "fe49d7f5b664907edb9b6e2ea874f31a8b4a427d58897435a6f743c93d8fe5bc"

def summarize_text(full_text):
    """Summarize the bill text using a Hugging Face summarization model."""
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    try:
        summary = summarizer(full_text, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]
        return summary
    except Exception as e:
        print(f"Failed to summarize text: {e}")
        return "No summary available."

def analyze_text_with_model(text):
    """Analyze text using Together AI or return a placeholder if unavailable."""
    try:
        response = requests.post(
            "https://api.together.xyz/v1/analyze",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={"text": text}
        )
        response.raise_for_status()
        together_output = response.json()
        return {
            "keywords": together_output.get("keywords", []),
            "analysis": together_output.get("analysis", "Analysis incomplete."),
        }
    except Exception as e:
        print(f"Together AI analysis failed: {e}")
        return {
            "keywords": [],
            "analysis": "Analysis failed due to an error.",
        }

def analyze_bills(bills):
    """Analyze a list of bills by summarizing and extracting insights."""
    analyses = []

    for bill in bills:
        try:
            # Combine title and summary for analysis
            title = bill.get("title", "No title")
            summary_text = bill.get("summary", "No summary")
            full_text = f"{title}. {summary_text}"

            # Summarize the bill
            summary = summarize_text(full_text)

            # Analyze the summary
            analysis_output = analyze_text_with_model(summary)

            analyses.append({
                "bill": title,
                "summary": summary,
                "keywords": analysis_output["keywords"],
                "analysis": analysis_output["analysis"],
            })
        except Exception as e:
            print(f"Error analyzing bill '{bill.get('title', 'Unknown')}': {e}")
            analyses.append({
                "bill": bill.get("title", "Unknown"),
                "analysis": "Analysis failed due to processing error.",
            })

    return analyses
