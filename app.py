from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the IV Rank API!"})

@app.route('/api/ivrank', methods=['GET'])
def get_iv_rank():
    url = "https://www.barchart.com/stocks/quotes/$DJX/overview"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        iv_rank_label = soup.find("span", text="IV Rank")
        if iv_rank_label:
            iv_rank_value = iv_rank_label.find_next("span", class_="right").text.strip()
            return jsonify({"IV Rank": iv_rank_value})

    return jsonify({"error": "IV Rank value not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
