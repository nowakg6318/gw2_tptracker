import requests
from bs4 import BeautifulSoup

#item_string = input('What items would you like to simulate?')
user_input_string = 'large claw,claw,vial of blood'
item_list =  user_input_string.split(',')
for item in item_list:
    item_word_list = item.split(' ')
    for i in range(len(item_word_list)):
        if item_word_list[i].lower() == 'of' or item_word_list[i].lower() == 'the':
            item_word_list[i] = item_word_list[i].lower()
        else:
            item_word_list[i] = (
                item_word_list[i][0].upper() + item_word_list[i][1:].lower())

    item_query_string = '_'.join(item_word_list)

    print(item_query_string)

    item_wiki_query_url = 'https://wiki.guildwars2.com/wiki/' + ' '.join(item_word_list)
    soup = BeautifulSoup(requests.get(item_wiki_query_url).content, 'html.parser')
    tag = soup.find(href=True, string='API')
    item_id = tag['href'][40:45]
