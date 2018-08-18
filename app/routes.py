from flask import render_template, request
from flask.json import jsonify
import requests

from app import app
from json import loads
from math import floor
from collections import OrderedDict
import pdb

@app.route('/_gettpdata')
def GetTPData():
  id_dict = {24295: 'Vial of Powerful Blood',
             24294: 'Vial of Potent Blood',  
             24293: 'Vial of Thick Blood',
             24292: 'Vial of Blood',
             24291: 'Vial of Thin Blood',
             24290: 'Vial of Weak Blood',
             24283: 'Powerful Venom Sac',
             24282: 'Potent Venom Sac',
             24281: 'Full Venom Sac',
             24280: 'Venom Sac',
             24279: 'Small Venom Sac',
             24278: 'Tiny Venom Sac',
             24296: 'Tiny Totem',
             24297: 'Small Totem',
             24298: 'Totem',
             24363: 'Engraved Totem',
             24299: 'Intricate Totem',
             24300: 'Elaborate Totem',
             24284: 'Tiny Scale',
             24285: 'Small Scale',
             24286: 'Scale',
             24287: 'Smooth Scale',
             24288: 'Large Scale',
             24289: 'Armored Scale',
             24352: 'Tiny Fang',
             24353: 'Small Fang',
             24354: 'Fang',
             24355: 'Sharp Fang',
             24356: 'Large Fang',
             24357: 'Vicious Fang',
             24272: 'Pile of Glittering Dust',
             24273: 'Pile of Shimmering Dust',
             24274: 'Pile of Radiant Dust',
             24275: 'Pile of Luminous Dust',
             24276: 'Pile of Incandescent Dust',
             24277: 'Pile of Crystalline Dust',
             24346: 'Tiny Claw',
             24347: 'Small Claw',
             24348: 'Claw',
             24349: 'Sharp Claw',
             24350: 'Large Claw',
             24351: 'Vicious Claw',
             24342: 'Bone Chip',
             24343: 'Bone Shard',
             24344: 'Bone',
             24345: 'Heavy Bone',
             24341: 'Large Bone',
             24358: 'Ancient Bone'}

  id_str = ''
  for value in id_dict.keys():
      id_str += str(value) + ','
  id_str = id_str[:-1]
  query_str = 'https://api.guildwars2.com/v2/commerce/listings?ids=' + id_str
  response = requests.get(query_str).content

  market_datalist = loads(response)
  market_datadict = {}

  for item_dict in market_datalist:
      estimated_profit_one = item_dict['sells'][0]['unit_price'] - item_dict['buys'][0]['unit_price'] - 0.15 *item_dict['sells'][0]['unit_price']
      estimated_profit_two = item_dict['sells'][1]['unit_price'] - item_dict['buys'][1]['unit_price'] - 0.15 *item_dict['sells'][1]['unit_price']
      market_datadict[id_dict[int(item_dict['id'])]] = [item_dict['buys'][0]['unit_price'], item_dict['sells'][0]['unit_price'], floor(estimated_profit_one)]

  ordered_market_datadict = OrderedDict(reversed(sorted(market_datadict.items(), key=lambda t:t[1][2])))
  return(jsonify(ordered_market_datadict))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
      text = request.form['items']
      item_list = text.strip().split(',')
      return(render_template('index.html', data=item_list))

    return(render_template('index.html'))


@app.route('/_ProcessItemList', methods=['GET', 'POST'])
def _ProcessItemList():
    if request.method == 'POST':
        item_list = ProcessItemList.text.strip().split(',')
        return(jsonify(item_list))
    
    else:
      print('Put some kind of exception here')
