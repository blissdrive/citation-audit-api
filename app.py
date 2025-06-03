from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Load your API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Citation Audit API is running!"

@app.route("/audit", methods=["POST"])
def audit():
    try:
        data = request.json
        print("📝 Incoming data:", data)

        # Safely extract fields with default values
        business_name = data.get("business-name", "Not Provided")
        address = data.get("address", "Not Provided")
        phone = data.get("phone", "Not Provided")
        website = data.get("website", "Not Provided")
        category = data.get("category", "Not Provided")
        email = data.get("your-email", "Not Provided")

        # Construct GPT prompt
        prompt = f"""
You are a local SEO expert. A business needs a citation audit and directory recommendations.

Business Name: {business_name}
Address: {address}
Phone: {phone}
Website: {website}
Category: {category}

1. Find 3 likely existing citations (e.g. Google, Yelp, MapQuest).
2. Recommend 5 core citation directories not listed.
3. Suggest 5 niche (beauty/wellness) citation directories.
4. Generate a plain-text report in this format:

📍 Existing Citations:
- Name: [Directory]
- URL: [Assumed or Common Listing URL]

✨ Citation Opportunities:
...

Thank you.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        result = response['choices'][0]['message']['content']
        return jsonify({
            "success": True,
            "report": result
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
