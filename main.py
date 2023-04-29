import os, requests, time, random
import json as json_lib
import colorama
from bs4 import BeautifulSoup

# init colorama
colorama.init()
session = requests.session()

# this script is used to check the stock of the flipper zero
# made by @Yuxontop
# bored to check joom stock

def changeLocalization(country_code):
    data = {
        "form_type": "localization",
        "utf8": "✓",
        "_method": "put",
        "return_to": "/",
        "country_code": str(country_code)
    }
    session.post("https://shop.flipperzero.one/localization", data=data)


def getStockCount(country_code="FR"):
    changeLocalization(country_code)
    stockint = ""

    cont = session.get('https://shop.flipperzero.one/').content

    cont = str(cont).split('''data-quantity-input>''')[1]
    cont = cont.split("</div>")[0]

    for i in cont:
        if str(i).isdigit():
            stockint += str(i)
    return int(stockint)

def checkForStocks():
    results = {}

    try:
        eu_stock = getStockCount()
    except:
        eu_stock = "Unknown"

    # Official Store

    
    FLIPPER_ZERO_URL = "https://shop.flipperzero.one/"
    HEADERS = {
        "set-cookie": "localization=FR; path=/; expires=Mon, 29 Apr 2024 13:42:57 GMT; SameSite=Lax",
        "cookie": """secure_customer_sig=; cart_currency=USD; _y=b4f2e600-d9b6-4f30-bf18-28380da74751; _shopify_y=b4f2e600-d9b6-4f30-bf18-28380da74751; _orig_referrer=https%3A%2F%2Fshop.flipperzero.one%2F; _landing_page=%2Fcart; cart=57d5301f394c6be8ceb2212948a45ce6; cbuid_meta={"referrer":"https://shop.flipperzero.one/cart","href":"https://shop.flipperzero.one/cart"}; __ddg1_=MAPEtVU76AVUKgiLW86J; _shopify_ga=undefined; _secure_session_id=f710ba52832e2db3064f08b5fb944c74; _s=f2f2a143-3e32-47cd-bdaf-f22e5051fcb4; _shopify_s=f2f2a143-3e32-47cd-bdaf-f22e5051fcb4; _shopify_sa_p=; keep_alive=24ec6dd3-6a22-451f-a855-3d7cb440136f; localization=DE; _shopify_sa_t=2023-04-29T13%3A42%3A55.390Z; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22USUSDE%22%2C%22sale_of_data_region%22%3Afalse%7D; mlveda_localization_country=FR; mlveda_localization_country_name=France; cart_ts=1682775777; cart_sig=ab348a1c6ce30e7887e6cff6a220e3c0; cart_ver=gcp-us-central1%3A12""",
        "accept-language": "fr-FR,fr;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(FLIPPER_ZERO_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    fp = soup.find_all('div', class_='featured-product__price', recursive=True)

    # Check that none of the child elements of each <div> contain the text "Sold Out"
    for p in fp:
        if any(child for child in p.descendants if 'sold out' in str(child).lower()):
            results["FlipperZero"] = {"Available": False, "Stock": "Out of stock"}
    
    results["FlipperZero"] = {"Available": True, "Stock": eu_stock}

    # Lab401

    try:
        json = session.get('https://lab401.com/fr/products/flipper-zero.js').json()
        if json['available'] == True:
            results["Lab401"] = {"Available": True, "Stock": eu_stock}
        else:
            results["Lab401"] = {"Available": False, "Stock": "Out of stock"}
    except:
        results["Lab401"] = {"Available": "Unknow", "Stock": "???"}
    
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        content = session.get('https://hackerwarehouse.com/product/flipper-zero/', headers=headers).content

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
            results["HackerWarehouse"] = {"Available": True, "Stock": eu_stock}
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
        print(colorama.Fore.WHITE + f"                     > Shop: {colorama.Fore.BLUE}{key}{colorama.Fore.WHITE} - Is Available: {colorama.Fore.GREEN if value['Available'] == True else colorama.Fore.RED}{value['Available']}{colorama.Fore.WHITE} - Stock: {colorama.Fore.YELLOW}{value['Stock']}{colorama.Fore.RESET}")

    # count down to down to 10 seconds in the ter
    print('\n'*6)
    ncs = random.randint(10, 25)
    for i in range(0, ncs, 1):
        print(colorama.Fore.CYAN + " "*20 + f"            Last check: {i} second(s) // Next check in {ncs-i} second(s)" + " "*20 + colorama.Fore.RESET, flush=True, end='\r')
        time.sleep(1)
