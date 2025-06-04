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

        # Refined and structured GPT prompt
        prompt = f"""
You are a local SEO and citation expert. A business needs a detailed citation audit and directory suggestions.

Business Details:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

Task:
1. Based on the business name, website, and category, list 5–10 likely existing citations (with assumed URLs if known) in this format:
   - Platform: [Name]
   - URL: [Likely or known listing]
   - Status: Likely Exists

2. List 5–10 core directories the business is not yet listed on. Use this format:
   - Platform: [Name]
   - Description: [One-line purpose of the site]
   - Free or Paid: [Free / Paid]
   - URL: [submission or homepage]

3. Based on the category "{category}", list 10–20 niche citation directories relevant to the industry. For each, include:
   - Platform Name
   - Short Description
   - Free or Paid
   - URL (homepage or submission link)

4. Separate each section with clear headers:
   📍 Existing Citations  
   🔎 Core Citation Opportunities  
   🧠 Niche Citation Directories

Only include platforms relevant to the category — do not suggest wellness/beauty directories for attorneys, landscapers, etc.

Return the response in plain text (no HTML).
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
