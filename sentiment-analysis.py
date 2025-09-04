import json
import time
from run_prompt import execute_gemini

# Load extracted tweets
with open("extracted_tweets.json", "r", encoding="utf-8") as extracted_tweets_file:
    extracted_tweets = json.load(extracted_tweets_file)

analyzed_tweets = []

# Process each tweet
for i, tweet in enumerate(extracted_tweets, start=1):
    sentiment_analysis_prompt = f"""
Tweet: {tweet["text"]}
like_count: {tweet["public_metrics"]["like_count"]}
retweet_count: {tweet["public_metrics"]["retweet_count"]}
reply_count: {tweet["public_metrics"]["reply_count"]}
impression_count: {tweet["public_metrics"]["impression_count"]}

Read the tweet with regard to its public reception and provide keywords and sentiment analysis score in JSON format like:
{{
  "keywords": [...],
  "sentiment_score": <number>
}}
""".strip()

    out = execute_gemini(sentiment_analysis_prompt)

    try:
        out_dict = json.loads(out)
    except json.JSONDecodeError:
        print("⚠️ Warning: Gemini output is not valid JSON:", out)
        continue

    # Add original tweet text
    out_dict["tweet"] = tweet["text"]

    # Append to results
    analyzed_tweets.append(out_dict)

    # Progress info
    print(f"✅ Processed tweet {i}/{len(extracted_tweets)}")

    # Sleep to avoid hitting API rate limit (15 req/min free tier)
    time.sleep(5)  # 5 seconds = max 12 requests per minute

# Save results
with open("analyzed_tweets.json", "w", encoding="utf-8") as analyzed_tweets_file:
    json.dump(analyzed_tweets, analyzed_tweets_file, indent=4, ensure_ascii=False)

print("🎉 Analysis saved to analyzed_tweets.json")
