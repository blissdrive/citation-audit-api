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

        # 🔁 Enhanced prompt (unlimited output)
        prompt = f"""
You are a local SEO expert and citation directory analyst.

Please generate a comprehensive citation audit and listing report for the following business:

Business Details:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

Your task is to return an extensive and detailed citation report broken into 3 sections:

📍 Existing Citations:
- List all known or highly likely existing citation listings for this business.
- Format: Platform, URL, Description
- Include at least 10–20+ listings across review platforms, maps, directories, aggregators, and booking tools.

🔎 Core Citation Opportunities:
- List every major core citation platform used in local SEO.
- Format: Platform, Description, Free or Paid, Submission URL
- Do not limit to just 5–10. Include as many as are appropriate globally and regionally.

🧠 Niche Citation Directories:
- Based on the category "{category}", list all niche-specific citation directories, industry platforms, associations, and aggregators.
- Format: Platform, Short Description, Free or Paid, Submission URL
- Include 25–100+ if applicable.
- Only include platforms that are relevant to the category — skip beauty/wellness unless the business is in that field.

Return your response in plain text, no HTML. Use clear headers for each section. Be exhaustive.
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
