import requests
import asyncio
import sys




BINANCE_P2P_API = "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

async def get_price(trade_type, fiat, token,cantidad):
    best_prices = []
    page = 1

    while True:
        request_body = {
            "page": page,
            "rows": 10,
            "payTypes": [],
            "asset": token,
            "tradeType": trade_type,
            "fiat": fiat,
            "publisherType": None,
            "merchantCheck": False,
            "transAmount ": cantidad
        }

        response = requests.post(BINANCE_P2P_API, json=request_body).json()
        data = response["data"]

        if not data:
            break

        all_prices = []
        users = []

        for order in data:
            adv = order["adv"]
            advertiser = order["advertiser"]

            user_no = advertiser["userNo"]
            real_name = advertiser["realName"]
            nick_name = advertiser["nickName"] if real_name is None else advertiser["realName"]

            if len(adv["tradeMethods"]) == 1:
                if adv["tradeMethods"][0]["identifier"] != "CashInPerson":
                    all_prices.append(float(adv["price"]))
                    users.append({
                        "user_no": user_no,
                        "nickname": nick_name,
                        "min_sell_quantity": float(adv["minSingleTransAmount"]),
                        "available_quantity": float(adv["surplusAmount"]),
                        "price": float(adv["price"]),
                        "banks": [adv["tradeMethods"][0]["tradeMethodName"]],
                        "sell_currency": adv["asset"],
                        "buy_currency": adv["fiatUnit"],
                    })
                continue

            banks = [method["tradeMethodName"] for method in adv["tradeMethods"] if method["identifier"] != "CashInPerson"]
            all_prices.append(float(adv["price"]))
            users.append({
                "user_no": user_no,
                "nickname": nick_name,
                "min_sell_quantity": float(adv["minSingleTransAmount"]),
                "available_quantity": float(adv["surplusAmount"]),
                "price": float(adv["price"]),
                "banks": banks if banks else ["Multiple"],
                "sell_currency": adv["asset"],
                "buy_currency": adv["fiatUnit"],
            })

        best_price = min(all_prices)
        best_prices.append({"price": best_price, "token": token, "users": users})

        page += 1

    return best_prices

async def get_buy_prices(trade_type, fiat, token,cantidad):
    buy_prices = await get_price(trade_type, fiat, token,cantidad)
    return buy_prices

async def get_sell_prices(trade_type, fiat, token,cantidad):
    sell_prices = await get_price(trade_type, fiat, token,cantidad)
    return sell_prices

async def main():
    trade_type = input("Enter trade type (SELL or BUY): ")
    fiat = input("Enter fiat currency (e.g., USD): ")
    token = input("Enter token: 'USDT','BTC','BUSD','BNB','ETH','DAI': ")
    cantidad =int(input("Cantidad a Comercializar ej.100: "))

    if trade_type=="SELL":
        sell_prices = await get_sell_prices(trade_type, fiat, token,cantidad)
        print("COMPRADORES ---->>> Sell Prices:")
        for sell_price in sell_prices:
            print(f"Token: {sell_price['token']}")
            print(f"Best Price: {sell_price['price']}")
            print("Users:")
            for user in sell_price['users']:
                nickname = user['nickname']
                nickname = nickname.encode('ascii', 'ignore').decode('ascii')
                print("Nickname:", nickname)
                print("Min Sell Quantity:", user['min_sell_quantity'])
                print("Available Quantity:", user['available_quantity'])
                print("Price:", user['price'])
                print("Bank(s):")
                for bank in user['banks']:
                    try: 
                        encoded_bank = bank.encode('ascii', 'ignore').decode('ascii')
                        bank=encoded_bank
                    except:
                        pass
                    print(bank)
                print("Sell Currency:", user['sell_currency'])
                print("Buy Currency:", user['buy_currency'])
                print("--------------------------------------")
    elif trade_type =="BUY":
        buy_prices = await get_buy_prices(trade_type, fiat, token,cantidad)
        print("VENDEDORES ------>> Buy Prices:")
        for buy_price in buy_prices:
            print(f"Token: {buy_price['token']}")
            print(f"Best Price: {buy_price['price']}")
            print("Users:")
            for user in buy_price['users']:
                nickname = user['nickname']
                nickname = nickname.encode('ascii', 'ignore').decode('ascii')
                print("Nickname:", nickname)
                print("Min Sell Quantity:", user['min_sell_quantity'])
                print("Available Quantity:", user['available_quantity'])
                print("Price:", user['price'])
                print("Bank(s):")
                for bank in user['banks']:
                    try: 
                        encoded_bank = bank.encode('ascii', 'ignore').decode('ascii')
                        bank=encoded_bank
                        #bank.encode("utf-8")
                    except:
                        pass
                    print(bank)
                print("Sell Currency:", user['sell_currency'])
                print("Buy Currency:", user['buy_currency'])
                print("------------------------------------")

    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
