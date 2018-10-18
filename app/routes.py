from flask import render_template, request, redirect, url_for, session
from flask.json import jsonify

from app import app

from app.webfunctions import ScrubUserText, FindItemNumber, ProcessItemName, GetMarketData, CalculateMarketEstimates


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def Homepage():
    if request.method == 'POST':
        return(redirect(url_for('CalculateArbitrage', user_data=request.form['items'])))
    else:
        return(render_template('index.html'))


@app.route('/bad_character', methods=['GET', 'POST'])
def BadCharPage():
    print(request.method)
    if request.method == 'POST':
        return(redirect(url_for('CalculateArbitrage', user_data=request.form['items'])))
    else:
        return(render_template('bad_character.html'))


@app.route('/bad_item_name', methods=['GET', 'POST'])
def BadItemNamePage():
    if request.method == 'POST':
        return(redirect(url_for('CalculateArbitrage', user_data=request.form['items'])))
    else:
        return(render_template('bad_item_name.html'))


@app.route('/calculations', methods=['GET', 'POST'])
def CalculateArbitrage():

    if request.args['user_data'] != '':
      item_list = ScrubUserText(request.args['user_data'])
    else:
      item_list = crafting_item_list

    if not item_list:
        return(redirect(url_for('BadCharPage')))

    item_id_list = []
    item_name_list = []
    for item_name in item_list:
        item_query_name = ProcessItemName(item_name)
        item_id = FindItemNumber(item_query_name)
        if not item_id:
            return(redirect(url_for('BadItemNamePage')))
        item_id_list.append(item_id)
        item_name_list.append(item_name)
    session['items_dict'] = dict(zip(item_id_list, item_name_list))
    return(redirect(url_for('MarketDataPage')))


@app.route('/_gettpdata')
def GetTPData():
    market_list = GetMarketData(session['items_dict'])
    market_dict = CalculateMarketEstimates(market_list, session['items_dict'])
    return(jsonify(market_dict))


@app.route('/market_data', methods=['GET'])
def MarketDataPage():
    return(render_template('tp_table.html'))


crafting_item_list = (['Vial of Powerful Blood',
           'Vial of Potent Blood',  
           'Vial of Thick Blood',
           'Vial of Blood',
           'Vial of Thin Blood',
           'Vial of Weak Blood',
           'Powerful Venom Sac',
           'Potent Venom Sac',
           'Full Venom Sac',
           'Venom Sac',
           'Small Venom Sac',
           'Tiny Venom Sac',
           'Tiny Totem',
           'Small Totem',
           'Totem',
           'Engraved Totem',
           'Intricate Totem',
           'Elaborate Totem',
           'Tiny Scale',
           'Small Scale',
           'Scale',
           'Smooth Scale',
           'Large Scale',
           'Armored Scale',
           'Tiny Fang',
           'Small Fang',
           'Fang',
           'Sharp Fang',
           'Large Fang',
           'Vicious Fang',
           'Pile of Glittering Dust',
           'Pile of Shimmering Dust',
           'Pile of Radiant Dust',
           'Pile of Luminous Dust',
           'Pile of Incandescent Dust',
           'Pile of Crystalline Dust',
           'Tiny Claw',
           'Small Claw',
           'Claw',
           'Sharp Claw',
           'Large Claw',
           'Vicious Claw',
           'Bone Chip',
           'Bone Shard',
           'Bone',
           'Heavy Bone',
           'Large Bone',
           'Ancient Bone'])