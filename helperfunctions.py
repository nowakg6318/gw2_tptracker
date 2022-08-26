''' A module containing web functions used in the guild wars 2 trading
post tracker program.

'''

def ScrubUserText(user_input_text):
    ''' Function to be deleted.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    '''
    for char in user_input_text:
        if (char.isalpha() or char==',' or char==' '):
            pass
        else:
            return([])
    item_list =  user_input_text.split(',')

    for item in item_list:
        item_list[item_list.index(item)] = item.strip()
    return(item_list)


def ProcessItemName(item_name):
    ''' Process the human readable gw2 item into a queryable format.

    Process the human readable gw2 item into a queryable format.  Mostly
    this means getting rid of 'the' and 'of' in the item name.

    Args:
        item_name (str): The gw2 item name.  Ex: "Vicious Claw"

    Returns:
        str: The queryable string of the gw2 item.  Ex: "viciousclaw"

    '''

    item_word_list = item_name.split(' ')
    for i in range(len(item_word_list)):
        if item_word_list[i].lower() == 'of' or item_word_list[i].lower() == 'the':
            item_word_list[i] = item_word_list[i].lower()
        else:
            item_word_list[i] = (
                item_word_list[i][0].upper() + item_word_list[i][1:].lower())

    item_query_name = '_'.join(item_word_list)
    return(item_query_name)


def FindItemNumber(item_query_name):
    ''' Get the gw2 item number for a specific gw2 item.

    Query gw2 wiki to find the gw2 in-game item number that corresponds to the
    human readable gw2 item name.

    Args:
        item_query_name (str): The queryable gw2 item string.

    Returns:
        int:  The gw2 item number corresponding to the gw2 queryable item 
        name.

    '''

    import requests
    from bs4 import BeautifulSoup

    item_wiki_query_url = 'https://wiki.guildwars2.com/wiki/' + ''.join(item_query_name)
    query = requests.get(item_wiki_query_url)
    if (query.status_code == 404) or ('API' not in str(query.content)):
        print(1)
        return(False)
    soup = BeautifulSoup(query.content, 'html.parser')
    tag = soup.find(href=True, string='API')
    item_id = tag['href'][40:45]
    return(item_id)


def ProcessInput(item_list):
    ''' Processes a large list of gw2 item names into a dictionary with their
    item number.

    Process a large list of gw2 items through other functions defined in this
    file to create a dictionary of the given items.

    Args:
        item_list (List[str]): A list of gw2 items.

    Returns:
        Dict[list]: A dictionary where the keys are gw2 items and the values
        are their associated gw2 iten numbers.

    '''

    item_id_list = [0]*len(item_list)
    item_qeury_name_list = [0]*len(item_list)
    for index, item_name in enumerate(item_list):
        item_query_name =ProcessItemName(item_name)
        item_id = FindItemNumber(item_query_name)
        if not item_id:
            raise RuntimeError('''Item ID not found.  
                               Please check the spelling of your item names.''')
        item_id_list[index] = item_id
        item_qeury_name_list[index] = item_name
    item_dict = dict(zip(item_id_list, item_qeury_name_list))
    return(item_dict)

def GetMarketData(items_dict):
    ''' Gets market data for a dictionary of gw2 item numbers.
    '''

    from json import loads
    import requests

    id_str = ''
    for value in items_dict.keys():
      id_str += value + ','
    id_str = id_str[:-1]
    query_str = 'https://api.guildwars2.com/v2/commerce/listings?ids=' + id_str
    response = requests.get(query_str).content
    market_list = loads(response)
    return(market_list)


def CalculateMarketEstimates(market_list, items_dict):

    from math import floor

    market_dict = {}
    for item_dict in market_list:
        item_name = items_dict[str(item_dict['id'])]
        estimated_profit_one = item_dict['sells'][0]['unit_price'] - item_dict['buys'][0]['unit_price'] - 0.15 *item_dict['sells'][0]['unit_price']
        estimated_profit_two = item_dict['sells'][1]['unit_price'] - item_dict['buys'][1]['unit_price'] - 0.15 *item_dict['sells'][1]['unit_price']
        market_dict[item_name] = [item_dict['buys'][0]['unit_price'], item_dict['sells'][0]['unit_price'], floor(estimated_profit_one)]

    market_dict = dict(reversed(sorted(market_dict.items(), key=lambda t:t[1][2])))
    return(market_dict)


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
           'Ancient Bone',
           'Green Wood Log',
           'Soft Wood Log',
           'Seasoned Wood Log',
           'Hard Wood Log',
           'Elder Wood Log',
           'Ancient Wood Log',
           'Copper Ore',
           'Silver Ore',
           'Gold Ore',
           'Iron Ore',
           'Platinum Ore',
           'Mithril Ore',
           'Orichalcum Ore',
           'Rawhide Leather Section',
           'Thin Leather Section',
           'Coarse Leather Section',
           'Rugged Leather Section',
           'Thick Leather Section',
           'Hardened Leather Section',
           'Jute Scrap',
           'Wool Scrap',
           'Cotton Scrap',
           'Linen Scrap',
           'Silk Scrap',
           'Gossamer Scrap'])