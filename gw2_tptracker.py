''' The main function of the gw2 trading post tracker program.

This program gets real time gw2 trading post data for many different basic
items and calculates the estimated profit if one were to buy at the highest
possible available price and sell at the lowest possible available price.
The data is then stored in an excel file in the same directory, sorted by
estimated profit.
'''

def main():
    import pandas as pd
    import helperfunctions as hf 

    item_list = hf.crafting_item_list
    item_dict = hf.ProcessInput(item_list)
    market_list = hf.GetMarketData(item_dict)
    market_dict = hf.CalculateMarketEstimates(market_list, item_dict)
    df = pd.DataFrame.from_dict(market_dict, orient='index',
                                columns=['Buy Price', 'Sell Price', 'Profit'])
    df.sort_values('Profit', ascending=False)
    #print(df)
    df.to_excel('text.xlsx')

if __name__ == '__main__':
    main()