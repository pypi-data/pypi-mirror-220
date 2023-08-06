"""
	This is a demo python script to show how to connect to Binance Spot Websocket API server,
	and how to send most common messages. This example already includes 2 messages:
	- get_market     Subscribe to Market data
	- get_orders     Subscribe order updates, and order records
	- get_params     Get request parameters

	You can just call each of message, it should work out of the box.
	It should also very convenient to be modified to call other endpoints.

	Notes:
	- websokcet-client package is required, you can install by: pip install websocket-client
	- API key and secret are required for endpoints that require signature

"""
import hmac
import json
import hashlib
import websocket

# If you like to run in debug mode
websocket.enableTrace(False)


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
			"third_identity_id": "ZCStreamingLiquidity1",
			"data_type": data_type,
		}

		signature = self.hashing(params["third_identity_id"])
		params['signature'] = signature
		return params

	def on_open(self, wsapp):
		print("connection open")

	def on_message(self, wsapp, message):
		message = json.loads(message)
		if message.get('error_code'):
			print(f"Error {message}")
			print("connection closed")
			return
		if not message.get('channel'):
			return
		print("Receiving message from server:", message)

	def on_error(self, wsapp, error):
		print(error)

	def on_close(self, wsapp, close_status_code, close_msg):
		print("Connection close")
		print(close_status_code)
		print(close_msg)

	def on_ping(self, wsapp, message):
		print("received ping from server")

	def on_pong(self, wsapp, message):
		print("received pong from server")

	def get_orders(self):
		params = self.get_params(channel="orders")
		wss_url = f'wss://dma-api.defi.wiki/ws/GetOrdersInfo?api_key={params["api_key"]}&third_identity_id={params["third_identity_id"]}&signature={params["signature"]}&data_type={params["data_type"]}'
		wsapp = websocket.WebSocketApp(wss_url,
										on_message=self.on_message,
										on_open=self.on_open,
										on_error=self.on_error,
										on_ping=self.on_ping,
										on_pong=self.on_pong)
		wsapp.run_forever()

	def get_market(self):
		params = self.get_params(channel="market")
		wss_url = f'wss://dma-api.defi.wiki/ws/GetMarket?api_key={params["api_key"]}&third_identity_id={params["third_identity_id"]}&signature={params["signature"]}&data_type={params["data_type"]}'
		wsapp = websocket.WebSocketApp(wss_url,
										on_message=self.on_message,
										on_open=self.on_open,
										on_error=self.on_error,
										on_ping=self.on_ping,
										on_pong=self.on_pong)
		wsapp.run_forever()


if __name__ == "__main__":
	apiKey = ""
	apiSecret = ""
	# ZerocapWebsocket(apiKey, apiSecret).get_orders()
	ZerocapWebsocketTest(apiKey, apiSecret).get_market()

# python -m pip install --user --upgrade setuptools wheel