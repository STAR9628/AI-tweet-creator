import pandas as pd
import json
from run_prompt import execute_gemini

# Function to select top 5 tweets by engagement type
def top_5_selection(analyzed_tweets, engagement_type: str):
    df = pd.DataFrame(analyzed_tweets)
    filtered_df = df[df['engagement_type'].str.lower() == engagement_type.lower()]
    return filtered_df.nlargest(5, columns=['engagement_score']).values.tolist()

# Function to create a new tweet
def create_tweet(analyzed_tweets):
    # Prompt with enforced JSON schema
    prompt = """
    You are a social media assistant.
    Task: Write a ready-to-post tweet for the newly releasing iPhone 17 Pro Max 
    with the A18 Pro SoC and physically moving camera zoom.
    The tweet must be short, catchy, and appealing to camera enthusiasts.

    ⚠️ IMPORTANT: Return ONLY valid JSON in this structure (all fields required):
    {
      "tweet_text": "string",
      "sentiment_type": "string",
      "engagement_type": "string",
      "sentiment_score": number,
      "topic": "string",
      "reason_for_engagement": "string",
      "engagement_score": number,
      "keywords": ["string"],
      "target_audience": "string"
    }
    """

    engagement_type = "Like"
    top_5_tweets = top_5_selection(analyzed_tweets, engagement_type)

    system_prompt = f"""
    Create an engaging Twitter post for my tech company.
    PROMPT: {prompt}
    Here are my top performing tweets for reference:
    {top_5_tweets}
    """

    response = execute_gemini(system_prompt)
    return response

if __name__ == "__main__":
    with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
        analyzed_tweets = json.load(f)

    tweet = create_tweet(analyzed_tweets)
    print("✅ Generated Tweet:\n", tweet)

    try:
        tweet_json = json.loads(tweet)

        # Fallback: if tweet_text missing, auto-generate from topic + keywords
        if "tweet_text" not in tweet_json or not tweet_json["tweet_text"].strip():
            keywords_str = " ".join(tweet_json.get("keywords", []))
            tweet_json["tweet_text"] = f"🚀 The new {tweet_json.get('topic','iPhone 17 Pro Max')} is here! {keywords_str}"

        print("\n📢 Ready-to-post Tweet:\n", tweet_json["tweet_text"])

    except Exception as e:
        print("\n❌ Error parsing JSON:", e)
