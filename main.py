from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=" + city
  res = requests.get(url).json()
  weather = res['today']

  return weather['weatherEnd'], math.floor(weather['tempMax']), math.floor(weather['tempMin']), weather["date"]

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_dujitang():
  words = requests.get("https://api.shadiao.pro/du")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_pengyouquan():
  words = requests.get("https://api.shadiao.pro/pyq")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color
  
def returnpinjie():
    return get_words() + "\n" + get_dujitang()+ "\n" + get_pengyouquan()
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, min_temperature, current_date = get_weather()
data = {
  "date": {"value": current_date, "color": generate_random_color()},
  "city": {"value": "临汾", "color": generate_random_color()},
  "weather":{"value":wea, "color": generate_random_color()},
  "temperature":{"value":temperature, "color": generate_random_color()},
  "min_temperature":{"value":min_temperature, "color": generate_random_color()},
  "love_days":{"value":get_count(), "color": generate_random_color()},
  "birthday_left":{"value": get_birthday(), "color": generate_random_color()},
  "Copywriting":{"value":returnpinjie(), "color": generate_random_color()},
}
res = wm.send_template(user_id, template_id, data)
print(res)
