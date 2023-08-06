"""
	This is a demo python script to show how to connect to Binance Spot Websocket API server,
	and how to send most common messages. This example already includes 2 messages:
	- get_market     Subscribe to Market data
	- get_orders     Subscribe order updates, and order records

	You can just call each of message, it should work out of the box.
	It should also very convenient to be modified to call other endpoints.

	Notes:
	- websokcet-client package is required, you can install by: pip install websocket-client
	- API key and secret are required for endpoints that require signature

"""
import hmac
import json
import hashlib
from websocket import create_connection


class ZerocapWebsocketTest:
	def __init__(self, apiKey, apiSecret):
		# TODO add your own API key and secret
		self.apiKey = apiKey
		self.apiSecret = apiSecret

	def hashing(self, query_string):
		return hmac.new(
			self.apiSecret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
		).hexdigest()

	def get_params(self, channel):
		'''
		Get request parameters
		:param channel:
		:return: params
		'''

		data_type = ""
		if channel == "orders":
			data_type = "order,trader"
		elif channel == "market":
			data_type = "price,order_book,k_line"

		params = {
			"api_key": self.apiKey,
			"data_type": data_type,
			"signature": self.hashing(self.apiKey)
		}
		return params

	def get_message(self, ws_recv):
		'''
		:param ws_recv:
		:return: message
		'''
		return ws_recv.__next__()

	def get_orders(self):
		params = self.get_params(channel="orders")
		wss_url = f'wss://dma-api.defi.wiki/ws/GetOrdersInfo?api_key={params["api_key"]}&signature={params["signature"]}&data_type={params["data_type"]}'
		ws = create_connection(wss_url)
		while True:
			message = ws.recv()
			yield message

	def get_market(self):
		params = self.get_params(channel="market")
		wss_url = f'wss://dma-api.defi.wiki/ws/GetMarket?api_key={params["api_key"]}&signature={params["signature"]}&data_type={params["data_type"]}'
		websocket = create_connection(wss_url)
		while True:
			message = websocket.recv()
			yield message


if __name__ == "__main__":
	apiKey = ""
	apiSecret = ""
	# ws = ZerocapWebsocketTest(apiKey, apiSecret)
	# websocket = ws.get_orders()
	# websocket = ws.get_market()
	# while True:
	# 	print(ws.get_message(websocket))



# pip install zerocap-websocket-test -i https://www.pypi.org/simple/