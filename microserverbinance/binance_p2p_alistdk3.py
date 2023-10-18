import requests

BINANCE_P2P_API = "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

async def get_price():
    TOKENS = ["USDT", "BUSD", "DAI", "ETH", "BTC", "BNB"]
    best_prices = []

    for token in TOKENS:
        # REQUEST BODY
        request_body = {
            "page": 1,
            "rows": 10,
            "payTypes": [],
            "asset": token,
            "tradeType": "BUY",
            "fiat": "USD",
            "publisherType": None,
            "merchantCheck": False,
        }

        response = requests.post(BINANCE_P2P_API, json=request_body).json()
        data = response["data"]

        all_prices = []
        users = []

        for order in data:
            adv = order["adv"]
            advertiser = order["advertiser"]
            
            # Extrae la información del usuario del diccionario "advertiser"
            user_no = advertiser["userNo"]
            real_name = advertiser["realName"]
            nick_name = advertiser["nickName"] if real_name is None else advertiser["realName"]
            
            # VERIFIED TRADE METHOD
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

    return best_prices


async def get_buy_prices():
    buy_prices = await get_price()
    return buy_prices


async def main():
    buy_prices = await get_buy_prices()

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
                print(bank)
            print("Sell Currency:", user['sell_currency'])
            print("Buy Currency:", user['buy_currency'])
            print()


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
