import json
import tornadoredis
from tornado import gen,web, websocket
from tornado.httpclient import AsyncHTTPClient
c = tornadoredis.Client()
ttl = 5

class MainHandler(web.RequestHandler):
    async def get(self):
        if await gen.Task(c.exists, 'rates'):
            res = await gen.Task(c.get, 'rates')
        else:
            http_client = AsyncHTTPClient()
            response = await http_client.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
            res_dict = json.loads(response.body.decode())
            res = res_dict['bpi']['USD']['rate']
        await gen.Task(c.set,'rates', res, ttl)
        self.write('Bitcoin curs is %s$' %res)

class TradeWebSockets(websocket.WebSocketHandler):
    def connect(self):
        '''new trade connection'''
        pass
    @gen.coroutine
    def message(self,message):
        pass
    def disconnect(self):
        '''closed trade connection'''
        pass