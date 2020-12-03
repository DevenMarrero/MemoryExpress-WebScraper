from MemoryExpressScraper import Scraper
import ast
config = open(__file__[:-7] + 'Config.txt').readlines()

for line in config:
    if "'sender'" in line:
        try:
            sender = ast.literal_eval(line)
            user = sender['sender']
            password = sender['password']
        except:
            pass

    elif "@" in line:
        emails = ast.literal_eval(line)

for line in config:
    if "'URL'" in line:
        try:
            settings = ast.literal_eval(line)

            URL = settings['URL']
            budgetLow = settings['budgetLow']
            budgetHigh = settings['budgetHigh']
            filterSale = settings['filterSale']

            search = Scraper(URL, budgetLow, budgetHigh, filterSale)
            search.run()
            search.send_email(user, password, emails)
        except:
            pass
