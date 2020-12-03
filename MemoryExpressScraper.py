import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage


class Scraper:
    def __init__(self, url, low, high, sale):
        self.URL = url
        self.LOW = low
        self.HIGH = high
        self.SALE = sale
        self.body = ''

    def run(self):
        items = self.get_page().find_all(class_='c-shca-icon-item')
        productsInfo = self.get_info(items)

        classProducts = []
        for i in productsInfo:
            classProducts.append(StoreProduct(i[0], i[1], i[2]))

        emailProducts = []
        for finalProduct in classProducts:
            try:
                emailProducts.append(("".join(finalProduct.return_info(self.HIGH, self.LOW, self.SALE))))
            except TypeError:
                pass
        self.body = ("\n".join(emailProducts))
        print(self.body)

    def get_page(self):
        print("Accessing Page...")
        try:
            page = requests.get(self.URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        except:
            raise ConnectionError("Error Connecting to Page!")

    def get_info(self, items):
        productlist = []
        for item in items:
            productlist.append(self.sort_info(item))
        return productlist

    @staticmethod
    def sort_info(item):
        name = (item.find(class_='c-shca-icon-item__body-name-brand').next_sibling.strip())

        unformSP = (item.find(class_='c-shca-icon-item__summary-rebate-savings').get_text())
        salePrice = (unformSP[unformSP.find("$"):(unformSP.find("$")) + 7])

        unformLP = (item.find(class_='c-shca-icon-item__summary-regular').get_text())
        listPrice = (unformLP[unformLP.find("$"):(unformLP.find("$")) + 7])
        return listPrice, salePrice, name

    def send_email(self, sender, password, to):
        self.body = self.body.replace("™", "").replace(" ", "  ").replace("   -", "  -")
        if self.SALE:
            showing = f"Showing products that are on sale between ${self.LOW} - ${self.HIGH}"
        else:
            showing = f"Showing all products between ${self.LOW} - ${self.HIGH}"

        if '&' in self.URL:
            search = self.URL[self.URL.find('=') + 1:self.URL.find('&')]
        else:
            search = self.URL[self.URL.find('=') + 1:]

        msg = EmailMessage()
        msg.set_content(f"\nSearch: {search.replace('+', ' ')} "
                        f"\nLink: {self.URL} "
                        f"\n{showing} "
                        f"\n\n"
                        f"{self.body} "
                        f"\n \n-Your Bot Program")
        msg['Subject'] = "Memory Express Search"
        msg['From'] = sender
        msg['To'] = to

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            print("Email Sent!")
        except:
            print("Something went wrong")


class StoreProduct:
    def __init__(self, price, sale, name):
        self.price = price
        self.priceInt = float(price[1:].replace(",", ""))
        self.sale = sale
        self.saleInt = float(sale[1:].replace(",", ""))
        self.name = name

        self.fix_format()

    def fix_format(self):
        if self.priceInt < 100:
            self.price = '$ ' + self.price[1:]

        if self.saleInt == self.priceInt:
            self.sale = "       "
        elif self.saleInt < 100:
            self.sale = '$ ' + self.sale[1:]

        self.name = '- ' + self.name

    def return_info(self, high, low, sale):
        if high >= self.saleInt >= low:
            return self.price + ' ', self.sale + ' ', self.name
