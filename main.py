import os, requests, time, random
import json as json_lib
import colorama
from bs4 import BeautifulSoup

# init colorama
colorama.init()

# this script is used to check the stock of the flipper zero
# made by @Yuxontop
# bored to check joom stock

def checkForStocks():
    results = {}

    # Official Store

    
    FLIPPER_ZERO_URL = "https://shop.flipperzero.one/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(FLIPPER_ZERO_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    fp = soup.find_all('div', class_='featured-product__price', recursive=True)

    # Check that none of the child elements of each <div> contain the text "Sold Out"
    for p in fp:
        if any(child for child in p.descendants if 'sold out' in str(child).lower()):
            results["FlipperZero"] = {"Available": False, "Stock": "Out of stock"}
    
    results["FlipperZero"] = {"Available": True, "Stock": '???'}

    # Lab401

    try:
        json = requests.get('https://lab401.com/fr/products/flipper-zero.js').json()
        if json['available'] == True:
            results["Lab401"] = {"Available": True, "Stock": "???"}
        else:
            results["Lab401"] = {"Available": False, "Stock": "Out of stock"}
    except:
        results["Lab401"] = {"Available": "Unknow", "Stock": "???"}
    
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        content = requests.get('https://hackerwarehouse.com/product/flipper-zero/', headers=headers).content

        # get the json data in the cart bundle_data bundle_data_35370 class
        soup = str(content).split('<div class="cart bundle_data bundle_data_35370" data-bundle_form_data="')[1]
        soup = str(soup).split('" data-bundle_id="35370">')[0]
        soup = soup.replace('&quot;', '"')

        json = json_lib.loads(soup)

        # get the stock

        s = json['has_variable_quantity']['70']
        q = json['quantities_available']["70"]
        if str(s).lower() == "no":
            results["HackerWarehouse"] = {"Available": False, "Stock": "Out of stock"}
        else:
            results["HackerWarehouse"] = {"Available": True, "Stock": int(q)}
    except:
        results["HackerWarehouse"] = {"Available": "Unknow", "Stock": "???"}

    return results


while True:
    stock = checkForStocks()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colorama.Fore.CYAN + "\n\n                                              Flipper Zero Stock Checker")
    print(colorama.Fore.CYAN + "                                                   Made by @yux" + colorama.Fore.RESET)
    print('\n'*6)
    for key, value in stock.items():
        print(colorama.Fore.WHITE + f"                     > Shop: {colorama.Fore.BLUE}{key}{colorama.Fore.WHITE} - Is Available: {colorama.Fore.GREEN if value['Available'] == True else colorama.Fore.RED}{value['Available']}{colorama.Fore.WHITE}")

    # count down to down to 10 seconds in the ter
    print('\n'*6)
    ncs = random.randint(10, 25)
    for i in range(0, ncs, 1):
        print(colorama.Fore.CYAN + " "*20 + f"            Last check: {i} second(s) // Next check in {ncs-i} second(s)" + " "*20 + colorama.Fore.RESET, flush=True, end='\r')
        time.sleep(1)
