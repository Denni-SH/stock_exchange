import tornadoredis
from tornado import gen,web, websocket
from tornado.httpclient import AsyncHTTPClient
import json

c = tornadoredis.Client()
ttl = 5

def json_save(new_order):
    orders_file = open('orders.json', 'r+', encoding='utf-8')
    orders_list = json.load(orders_file)
    orders_file.close()
    order_file = open('orders.json', 'w', encoding='utf-8')
    orders_list.append(new_order)
    json.dump(orders_list, order_file, ensure_ascii=False)
    order_file.close()


class AddOrder(web.RequestHandler):
    async def get(self):
        self.render('add_order.html')

    async def post(self, *args, **kwargs):
        type = self.get_argument('type')
        price = self.get_argument('price')
        quantity = self.get_argument('quantity')
        new_order = {'type': type, 'price': price, 'quantity': quantity}
        json_save(new_order)
        self.redirect("/")


class MainHandler(web.RequestHandler):
    async def get(self):
        self.render('index.html')


# class MainHandler(web.RequestHandler):
#     async def get(self):
#         if await gen.Task(c.exists, 'rates'):
#             res = await gen.Task(c.get, 'rates')
#         else:
#             http_client = AsyncHTTPClient()
#             response = await http_client.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
#             res_dict = json.loads(response.body.decode())
#             res = res_dict['bpi']['USD']['rate']
#         await gen.Task(c.set,'rates', res, ttl)
#         self.write('Держу в курсе, курс биткоина - %s$' %res)
#
#
# class TradeWebSockets(websocket.WebSocketHandler):
#     def connect(self):
#         '''new trade connection'''
#         pass
#     @gen.coroutine
#     def message(self,message):
#         pass
#     def disconnect(self):
#         '''closed trade connection'''
#         pass