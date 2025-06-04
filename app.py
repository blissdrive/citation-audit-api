from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS

# Load your API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask
app = Flask(__name__)
CORS(app, origins=["https://devtestsite.xyz"])

@app.route("/")
def index():
    return "✅ Citation Audit API is running!"

@app.route("/audit", methods=["POST"])
def audit():
    try:
        data = request.json
        print("📝 Incoming data:", data, flush=True)

        # Safely extract fields with default values
        business_name = data.get("business-name", "Not Provided")
        address = data.get("address", "Not Provided")
        phone = data.get("phone", "Not Provided")
        website = data.get("website", "Not Provided")
        category = data.get("category", "Not Provided")
        email = data.get("your-email", "Not Provided")

        # 🔁 Enhanced prompt with explicit table row counts
        prompt = f"""
You are a local SEO expert and citation research assistant.

Create a detailed citation audit report for this business, formatted in Markdown. Use the following structure and follow the exact formats below:

Business Details:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

1. ### 📍 Existing Citations
Output a Markdown table with 3 columns:
| Platform | URL | Description |
Include at least 50–100 known or likely existing citations (Google, Yelp, Facebook, BBB, MapQuest, etc.). Use assumed listing URLs if needed based on brand/location.

2. ### 🔎 Core Citation Opportunities
Output a Markdown table with 4 columns:
| Platform | Description | Free or Paid | Submission URL |
List 50–100 of the most important general citation directories for local SEO, including global and regional platforms.

3. ### 🧠 Niche Citation Directories
Based on the category "{category}", list 50–100+ relevant industry-specific citation sites, directories, associations, or aggregators.
Output a Markdown table with:
| Platform | Description | Free or Paid | Submission URL |

Only include platforms relevant to the industry — skip wellness/beauty unless the business category is in that field.

Return only Markdown. Do not use bullet points, paragraphs, or HTML. Be thorough.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=3000
        )

        result = response['choices'][0]['message']['content']
        print("📄 GPT Report:\n", result, flush=True)

        return jsonify({
            "success": True,
            "report": result
        })

    except Exception as e:
        print("❌ ERROR:", str(e), flush=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
