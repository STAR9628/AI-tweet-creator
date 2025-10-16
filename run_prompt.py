# To run this code you need to install the following dependencies:
# pip install google-genai

import os
import json
from google import genai
from google.genai import types

# ⚠️ API Key (replace if rotated)
GEMINI_API_KEY = "AIzaSyCAAb6uwoCG-yvedBqze6sppF62d6GHQbA"


# -------------------------------
# Creation: Single Tweet
# -------------------------------
def execute_gemini_for_tweet_creation(prompt: str, model: str = "gemini-2.5-flash-lite"):
    client = genai.Client(api_key=GEMINI_API_KEY)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["tweet", "prediction", "explanation"],
            properties={
                "tweet": genai.types.Schema(type=genai.types.Type.STRING),
                "prediction": genai.types.Schema(type=genai.types.Type.STRING),
                "explanation": genai.types.Schema(type=genai.types.Type.STRING),
            },
        ),
    )

    # Call Gemini
    result = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        print("⚠️ Gemini did not return valid JSON (tweet creation)")
        return {}


# -------------------------------
# Prediction: Compare Tweet A vs Tweet B
# -------------------------------
def execute_gemini_for_tweet_prediction(prompt: str, model: str = "gemini-2.5-flash-lite"):
    client = genai.Client(api_key=GEMINI_API_KEY)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["tweet_a_vs_tweet_b", "prediction", "explanation"],
            properties={
                "tweet_a_vs_tweet_b": genai.types.Schema(type=genai.types.Type.STRING),
                "prediction": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=["tweet_a", "tweet_b", "equal"],
                ),
                "explanation": genai.types.Schema(type=genai.types.Type.STRING),
            },
        ),
    )

    # Call Gemini
    result = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        print("⚠️ Gemini did not return valid JSON (tweet prediction)")
        return {}


# -----------------------
# 🚀 Example Usage
# -----------------------
if __name__ == "__main__":
    # Example: Generate two tweets and compare
    creation_prompt = """You are an expert social media strategist.
    Task: Write a ready-to-post tweet about the iPhone 17 Pro Max launch.
    ⚠️ Return ONLY JSON with: tweet, prediction, explanation
    """

    prediction_prompt = """You are given two tweets. Compare them for engagement, relevance, and audience relativeness.
    ⚠️ Return ONLY JSON with: tweet_a_vs_tweet_b, prediction, explanation
    Tweet A: The future is here! 🤯 iPhone 17 Pro Max drops with crazy new camera zoom.
    Tweet B: Apple launches iPhone 17 Pro Max with A18 Pro chip and moving zoom lens.
    """

    print("\n--- Tweet Creation ---")
    result_creation = execute_gemini_for_tweet_creation(creation_prompt)
    print(json.dumps(result_creation, indent=4, ensure_ascii=False))

    print("\n--- Tweet Prediction ---")
    result_prediction = execute_gemini_for_tweet_prediction(prediction_prompt)
    print(json.dumps(result_prediction, indent=4, ensure_ascii=False))
