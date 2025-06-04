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

        # 🔁 Enhanced prompt with Markdown tables
        prompt = f"""
You are a local SEO expert and citation directory analyst.

Please generate a comprehensive citation audit and listing report in Markdown format for the following business:

Business Details:
- Name: {business_name}
- Address: {address}
- Phone: {phone}
- Website: {website}
- Category: {category}

Your report must include three sections, each with a clear header and formatted tables:

### 📍 Existing Citations
| Platform | URL | Description |
|----------|-----|-------------|
- List as many known or highly likely citations as possible.

### 🔎 Core Citation Opportunities
| Platform | Description | Free or Paid | Submission URL |
|----------|-------------|--------------|----------------|
- List every general citation site suitable for local SEO.

### 🧠 Niche Citation Directories
| Platform | Description | Free or Paid | Submission URL |
|----------|-------------|--------------|----------------|
- Based on category "{category}", list all relevant niche-specific directories (25–100+).
- Include associations, aggregators, review platforms, and industry sites.
- Skip wellness/beauty unless the category is relevant.

Return the full response as Markdown with headers and tables — no HTML, no bullet lists, no code blocks. Be exhaustive.
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
