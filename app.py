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

        # 🔁 Enhanced prompt for GPT-4
        prompt = f"""
You are a local SEO expert and citation directory analyst.

Create a detailed citation audit report for the following business. Return your output in Markdown format only. Use clean tables under each section.

Business:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

Sections to include:

### 📍 Existing Citations
- Output a Markdown table: | Platform | URL | Description |
- Include at least 50 known or likely citations (Google, Yelp, BBB, Facebook, Apple Maps, etc.)

### 🔎 Core Citation Opportunities
- Output a Markdown table: | Platform | Description | Free or Paid | Submission URL |
- List 50+ essential core directories for general SEO

### 🧠 Niche Citation Directories
- Based on the category "{category}", list 50–100+ niche or industry-specific citation sources
- Output: | Platform | Description | Free or Paid | Submission URL |
- Only include platforms relevant to the business type. Skip unrelated categories.

Respond only with clean Markdown tables. No paragraphs, bullet points, or HTML.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096
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
