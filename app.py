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
        print("📝 Incoming data:", data, flush=True)

        # Safely extract fields with default values
        business_name = data.get("business-name", "Not Provided")
        address = data.get("address", "Not Provided")
        phone = data.get("phone", "Not Provided")
        website = data.get("website", "Not Provided")
        category = data.get("category", "Not Provided")
        email = data.get("your-email", "Not Provided")

         # Advanced GPT prompt with no output limits
        prompt = f"""
You are a local SEO and citation audit expert. Please generate a fully detailed citation audit report for the following business:

Business Details:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

Your task is to research and generate a structured, comprehensive audit that includes the following:

📍 Existing Citations:
- Find and list as many known and likely existing citation listings for the business as possible.
- Include the platform name, the assumed or known URL, and note if the listing is likely present or confirmed.

🔎 Core Citation Opportunities:
- List every major general citation platform that businesses should be listed on.
- For each one, include:
  - Platform name
  - Description
  - Free or Paid
  - Submission URL or homepage

🧠 Niche Citation Directories (Based on Category):
- Based on the category "{category}", find every relevant industry-specific citation platform or directory.
- These should include specialized business directories, industry associations, review platforms, etc.
- For each:
  - Platform name
  - Short description
  - Free or Paid
  - URL or submission link

Please be exhaustive. Include as many relevant platforms as you can in each section. Avoid any directories that are unrelated to the business category.

Respond in plain text, no HTML.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
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
