from rest_framework.response import Response
from upstox_api.api import Upstox
from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_market_data(request, symbol):
    # Initialize the Upstox API with your API Key
    api = Upstox('<YOUR_API_KEY>')

    # Fetch market data for a specific symbol
    market_data = api.get_live_feed(Upstox.Exchange.NSE, symbol)

    # Return the market data as a JSON response
    return Response(market_data)
