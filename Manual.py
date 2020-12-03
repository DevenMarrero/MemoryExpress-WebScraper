from MemoryExpressScraper import Scraper


def set_parameters():
    while True:
        print('Type "sale" to filter items on sale. 1 number will indicate max budget 2 will indicate min/max.')
        parameters = input(': ').lower().split()
        sale = False
        budgetParameters = []
        for parameter in parameters:
            try:
                budgetParameters.append(int(parameter))
            except ValueError:
                if 'sale' in parameter:
                    sale = True
        if len(budgetParameters) <= 2:
            break
        print("Budget can only consist of 1 or 2 values")

    if len(budgetParameters) == 1:
        high = max(budgetParameters)
        low = 0
    elif len(budgetParameters) == 2:
        high = max(budgetParameters)
        low = min(budgetParameters)
    else:
        high = 100000
        low = 0
    return high, low, sale


URL = input('Enter URL: ')
budgetHigh, budgetLow, filterSale = set_parameters()
search = Scraper(URL, budgetLow, budgetHigh, filterSale)
search.run()
