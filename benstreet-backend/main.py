from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="BenStreet API",
    version="1.0.0"
)

BASE_URL = "https://localhost:5000/v1/api"
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
session = requests.Session()
session.verify = False

def ibkr_get(endpoint):
    r = session.get(f"{BASE_URL}{endpoint}", timeout=10)

    # print("STATUS:", r.status_code)
    # print("RESPONSE:", r.text)
    r.raise_for_status()
    return r.json()

def ibkr_post(endpoint, payload=None):
    if payload is None:
        payload = {}

    r = session.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        timeout=10
    )

    # print("STATUS:", r.status_code)
    # print("RESPONSE:", r.text)

    r.raise_for_status()
    return r.json()

def market_is_open():

    now = datetime.now(
        ZoneInfo("America/New_York")
    )

    if now.weekday() >= 5:
        return False

    minutes = now.hour * 60 + now.minute

    return (
        9 * 60 + 30 <= minutes < 16 * 60
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {
        "status": "online",
        "time": datetime.now()
    }

@app.get("/api/status")
def auth_status():

    try:
        return ibkr_post("/iserver/auth/status")

    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/portfolio")
def portfolio():

    try:
        accounts = ibkr_get("/portfolio/accounts")

        if not accounts:
            raise HTTPException(
                status_code=404,
                detail="No IBKR accounts found."
            )

        positions = ibkr_get(
            f"/portfolio2/{ACCOUNT_ID}/positions?sort=marketValue&direction=d"
        )

        ledger = ibkr_get(f"/portfolio/{ACCOUNT_ID}/ledger")
        cash = float(ledger["USD"]["cashbalance"])

        return {
        "cash": cash,
        "positions": positions
        }

    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/api/buy")
def buy_stock(ticker: str):


    # -> We have to do this
    response = ibkr_get(
        "/iserver/accounts"
    )

    if not response:
            raise HTTPException(
                status_code=404,
                detail="No IBKR accounts found."
            )


    search = ibkr_get(
        f"/iserver/secdef/search?symbol={ticker}",
    )

    if not search:
        raise HTTPException(404, "Ticker not found")

    conid = search[0]["conid"]

    if market_is_open():

        ibkr_get(
            f"/iserver/marketdata/snapshot?conids={conid}&fields=31,84,86",
        )

        snapshot = ibkr_get(
            f"/iserver/marketdata/snapshot?conids={conid}&fields=31,84,86",
        )[0]

        last = float(snapshot.get("31") or 0)
        ask = float(snapshot.get("84") or last)
        bid = float(snapshot.get("86") or last)

        if ask <= 0:
            ask = last

        if ask <= 0:
            raise HTTPException(500, "No valid market price, try again now (this is a quirk of the API)")

        quantity = round(1.0 / ask, 4)


        limit_price = round(ask * 1.01, 2)

        payload = {
            "orders": [
                {
                    "acctId":ACCOUNT_ID,
                    "conid": int(conid),
                    "side": "BUY",
                    "orderType": "LMT",
                    "price": limit_price,
                    "quantity": quantity,
                    "tif": "DAY",
                    "outsideRTH": False
                }
            ]
        }
    
    else:
        raise HTTPException(
            status_code=400,
            detail="Market is closed."
        )

    response = ibkr_post(
        f"/iserver/account/{ACCOUNT_ID}/orders",
        payload
    )


    while (
        isinstance(response, list)
        and len(response) > 0
        and "id" in response[0]
    ):

        reply_id = response[0]["id"]

        response = ibkr_post(
            f"/iserver/reply/{reply_id}",
            {
                "confirmed": True
            }
        )

    return response

@app.post("/api/sell")
def sell_stock(ticker: str):

    # -> We have to do this
    response = ibkr_get(
        "/iserver/accounts"
    )

    if not response:
            raise HTTPException(
                status_code=404,
                detail="No IBKR accounts found."
            )

    # -> We ALSO have to do this


    accounts = ibkr_get("/portfolio/accounts")

    if not accounts:
        raise HTTPException(
            status_code=404,
            detail="No IBKR accounts found."
        )

    search = ibkr_get(
        f"/iserver/secdef/search?symbol={ticker}",
    )

    if not search:
        raise HTTPException(
            404,
            "Ticker not found"
        )

    conid = int(search[0]["conid"])

    positions = ibkr_get(
        f"/portfolio2/{ACCOUNT_ID}/positions?sort=marketValue&direction=d"
    )

    position = None

    for p in positions:
        if (
            # i guess conid has to cast to str
            p["conid"] == str(conid)
            and p["position"] > 0
        ):
            position = p
            break


    if position is None:
        raise HTTPException(
            400,
            "No position found"
        )


    shares_owned = float(position["position"])

    ibkr_get(
        f"/iserver/marketdata/snapshot?conids={conid}&fields=31,84,86",
    )

    snapshot = ibkr_get(
        f"/iserver/marketdata/snapshot?conids={conid}&fields=31,84,86",
    )[0]

    bid = float(
        snapshot.get("86")
        or snapshot.get("31")
    )


    quantity = round(
        1.0 / bid,
        4
    )

    quantity = min(
        quantity,
        shares_owned
    )


    if quantity <= 0:
        raise HTTPException(
            400,
            "Insufficient position"
        )

    limit_price = round(
        bid * 0.995,
        2
    )


    payload = {
        "orders": [
            {
                "acctId": ACCOUNT_ID,

                "conid": conid,

                "ticker": ticker,

                "orderType": "LMT",

                "side": "SELL",

                "tif": "DAY",

                "price": limit_price,

                "quantity": quantity,

                "outsideRTH": False
            }
        ]
    }


    response = ibkr_post(
        f"/iserver/account/{ACCOUNT_ID}/orders",
        payload
    )

    while (
        isinstance(response, list)
        and len(response) > 0
        and "id" in response[0]
    ):

        response = ibkr_post(
            f"/iserver/reply/{response[0]['id']}",
            {
                "confirmed": True
            }
        )


    return response

@app.get("/api/activity")
def get_activity():

    try:
        ibkr_get("/iserver/accounts")

        orders_response = ibkr_get(
            "/iserver/account/orders"
        )

        pending_orders = orders_response.get(
            "orders",
            []
        )

        trades_response = ibkr_get(
            "/iserver/account/trades"
        )

        activity = []

        # pending orders
        for order in pending_orders:

            # if order.get("status") != "submitted":
            if False:
                continue

            activity.append({

                "id": order.get("orderId"),

                "ticker": (
                    order.get("ticker")
                    or order.get("symbol")
                ),

                "side": order.get("side"),

                "type": "ORDER",

                "status": order.get("status"),

                "shares": order.get("size"),


                "price": (
                    order.get("avgPrice")
                    or order.get("price")
                ),

                "timestamp": order.get(
                    "lastExecutionTime_r"
                )

            })

        # completed orders
        for trade in trades_response:

            activity.append({

                "id": trade.get(
                    "execution_id"
                ),

                "ticker": (
                    trade.get("symbol")
                    or trade.get("ticker")
                ),

                "side": trade.get(
                    "side"
                ),

                "type": "TRADE",

                "status": "FILLED",

                "shares": trade.get(
                    "size"
                ),

                "price": trade.get(
                    "price"
                ),

                "timestamp": trade.get(
                    "trade_time_r"
                )

            })


        activity.sort(
            key=lambda x: x["timestamp"] or "",
            reverse=True
        )


        return activity[:10]


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )