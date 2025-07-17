from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

ebay_api_id = 'Alexandr-PriceIT-SBX-60bbd31c9-23a29497'


def get_price_stats(item):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    params = {
        'OPERATION-NAME': 'findItemsByKeywords',
        'SERVICE-VERSION': '1.0.0',
        'SECURITY-APPNAME': ebay_api_id,
        'RESPONSE-DATA-FORMAT': 'JSON',
        'REST-PAYLOAD': '',
        'keywords': item,
        'paginationInput.entriesPerPage': 10
    }
    response = requests.get(url, params=params)
    prices = []

    if response.status_code == 200:
        data = response.json()
        try:
            items = data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
            for i in items:
                price = float(i["sellingStatus"][0]["currentPrice"][0]["__value__"])
                prices.append(price)
        except Exception as e:
            print("Error parsing API response:", e)

    if prices:
        return {
            'item': item,
            'min': round(min(prices), 2),
            'max': round(max(prices), 2),
            'average': round(sum(prices)/len(prices), 2)
        }
    else:
        return {
            'item': item,
            'min': 'N/A',
            'max': 'N/A',
            'average': 'N/A'
        }



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/price', methods=['GET', 'POST'])
def price():
    stats= None 
    if request.method == 'POST':
        data = request.form.get('item')
        if data:
            stats = get_price_stats(data)
    return render_template('price.html', stats=stats)



if __name__ == '__main__':
    app.run(debug=True)
