from websocket import WebSocketApp
import time
import random
import json
import _thread as thread
import math

fire_rate = 0.4
bullet_radius = 25
player_radius = 50

fire_timer: float = 0
x = 0
y = 0
id = ''
url = 'wss://aispawn.herokuapp.com/ws'
# url = "ws://localhost:3000/ws"

def check_incoming(bullets, x, y):
  for b in bullets:
    # print(b['id'])
    new_x = b['x'] + b['angle'][0]
    new_y = b['y'] + b['angle'][1]

    if math.dist((new_x, new_y), (x, y)) <= (bullet_radius+player_radius)*1.5 and b['fired_by']!=id:
      ws.send(f'vel{random.randint(-100000,100000)},{random.randint(-100000,100000)}')
      ws.send('dash')


def ws_handler(ws, message):
  global fire_timer
  global x
  global y
  global id
  msg=json.loads(message)
  if msg['type']=='sync_player':
      
      this_player = msg['you_are']
      other = 1-this_player
      players = msg['info'][0]
      px = players[other]['x']
      py = players[other]['y']

      bx=players[this_player]['x']
      by=players[this_player]['y']
      id = players[this_player]['id']
      x = bx
      y = by
      if time.time() - fire_timer >= fire_rate:
        ws.send(f'fire{px-bx}, {py-by}')
        fire_timer=time.time()
      ws.send(f'vel{px-bx},{py-by}')
  if msg['type']=='sync_bullet':
    bullets = msg['info'][0]
    check_incoming(bullets, x, y)

def on_error(ws, error):
    print(error)

def on_open(ws):
    def run(*args):
      while True:
        time.sleep(0.1)
        ws.send('sync')
    ws.send('nameBotBoio')
    thread.start_new_thread(run, ())

ws = WebSocketApp(url, on_message=ws_handler, on_error = on_error)
ws.on_open = on_open
ws.run_forever()

