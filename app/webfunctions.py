''' A module containing web functions used in the gw2_tptrader web application.

'''

from typing import List,Dict

def ScrubUserText(user_input_text: str) -> List[str]:
    for char in user_input_text:
        if (char.isalpha() or char==',' or char==' '):
            pass
        else:
            return([])
    item_list =  user_input_text.split(',')

    for item in item_list:
        item_list[item_list.index(item)] = item.strip()
    return(item_list)


def ProcessItemName(item_name: str) -> str:

    item_word_list = item_name.split(' ')
    for i in range(len(item_word_list)):
        if item_word_list[i].lower() == 'of' or item_word_list[i].lower() == 'the':
            item_word_list[i] = item_word_list[i].lower()
        else:
            item_word_list[i] = (
                item_word_list[i][0].upper() + item_word_list[i][1:].lower())

    item_query_name = '_'.join(item_word_list)
    return(item_query_name)

def FindItemNumber(item_query_name: str) -> int:

    import requests
    from bs4 import BeautifulSoup

    item_wiki_query_url = 'https://wiki.guildwars2.com/wiki/' + ''.join(item_query_name)
    soup = BeautifulSoup(requests.get(item_wiki_query_url).content, 'html.parser')
    tag = soup.find(href=True, string='API')
    item_id = tag['href'][40:45]
    return(item_id)


def GetMarketData(items_dict: dict) -> List[Dict]:
    '''
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


def CalculateMarketEstimates(market_list: List[dict], items_dict: dict) -> dict:

    from math import floor

    market_dict = {}
    for item_dict in market_list:
        print(items_dict)
        item_name = items_dict[str(item_dict['id'])]
        estimated_profit_one = item_dict['sells'][0]['unit_price'] - item_dict['buys'][0]['unit_price'] - 0.15 *item_dict['sells'][0]['unit_price']
        estimated_profit_two = item_dict['sells'][1]['unit_price'] - item_dict['buys'][1]['unit_price'] - 0.15 *item_dict['sells'][1]['unit_price']
        market_dict[item_name] = [item_dict['buys'][0]['unit_price'], item_dict['sells'][0]['unit_price'], floor(estimated_profit_one)]

    market_dict = dict(reversed(sorted(market_dict.items(), key=lambda t:t[1][2])))
    return(market_dict)
