from flask import render_template, request, redirect, url_for, session
from flask.json import jsonify

from app import app

from app.webfunctions import ScrubUserText, FindItemNumber, ProcessItemName, GetMarketData, CalculateMarketEstimates

@app.route('/_gettpdata')
def GetTPData():
    print(2)
    market_list = GetMarketData(session['item_id_list'])
    market_dict = CalculateMarketEstimates(market_list)
    return(jsonify(market_dict))

  # id_dict = {24295: 'Vial of Powerful Blood',
  #            24294: 'Vial of Potent Blood',  
  #            24293: 'Vial of Thick Blood',
  #            24292: 'Vial of Blood',
  #            24291: 'Vial of Thin Blood',
  #            24290: 'Vial of Weak Blood',
  #            24283: 'Powerful Venom Sac',
  #            24282: 'Potent Venom Sac',
  #            24281: 'Full Venom Sac',
  #            24280: 'Venom Sac',
  #            24279: 'Small Venom Sac',
  #            24278: 'Tiny Venom Sac',
  #            24296: 'Tiny Totem',
  #            24297: 'Small Totem',
  #            24298: 'Totem',
  #            24363: 'Engraved Totem',
  #            24299: 'Intricate Totem',
  #            24300: 'Elaborate Totem',
  #            24284: 'Tiny Scale',
  #            24285: 'Small Scale',
  #            24286: 'Scale',
  #            24287: 'Smooth Scale',
  #            24288: 'Large Scale',
  #            24289: 'Armored Scale',
  #            24352: 'Tiny Fang',
  #            24353: 'Small Fang',
  #            24354: 'Fang',
  #            24355: 'Sharp Fang',
  #            24356: 'Large Fang',
  #            24357: 'Vicious Fang',
  #            24272: 'Pile of Glittering Dust',
  #            24273: 'Pile of Shimmering Dust',
  #            24274: 'Pile of Radiant Dust',
  #            24275: 'Pile of Luminous Dust',
  #            24276: 'Pile of Incandescent Dust',
  #            24277: 'Pile of Crystalline Dust',
  #            24346: 'Tiny Claw',
  #            24347: 'Small Claw',
  #            24348: 'Claw',
  #            24349: 'Sharp Claw',
  #            24350: 'Large Claw',
  #            24351: 'Vicious Claw',
  #            24342: 'Bone Chip',
  #            24343: 'Bone Shard',
  #            24344: 'Bone',
  #            24345: 'Heavy Bone',
  #            24341: 'Large Bone',
  #            24358: 'Ancient Bone'}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def Homepage():
    if request.method == 'POST':
        item_list = ScrubUserText(request.form['items'])
        item_number_list = []
        for item_name in item_list:
          item_query_name = ProcessItemName(item_name)
          item_number = FindItemNumber(item_query_name)
          item_number_list.append(int(item_number))
        session['item_id_list'] = item_number_list
        return(redirect(url_for('MarketDataPage')))

    else:
      return(render_template('index.html'))


@app.route('/market_data', methods=['GET'])
def MarketDataPage():
    return(render_template('tp_table.html'))


  

