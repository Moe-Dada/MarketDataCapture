import ccxt
import time
import schedule
from pymongo import MongoClient
from datetime import datetime

# -------------------------------------------------------------------
# 1. SET UP MONGODB CONNECTION
# -------------------------------------------------------------------
#MONGO_URI = "mongodb://localhost:27017/"  # or your MongoDB Atlas connection string
MONGO_URI = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.7/"

DATABASE_NAME = "market_data"
COLLECTION_NAME = "orderbooks"
SYMBOL_LIST = ["BTC/USDT", "ETC/USDT", "LTC/USDT", "XRP/USDT", "TRX/USDT", "SOL/USDT"]

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# -------------------------------------------------------------------
# 2. INITIALIZE THE EXCHANGE (BINANCE EXAMPLE)
# -------------------------------------------------------------------
exchange = ccxt.binance({
    "enableRateLimit": True  # Rate limits
})


# -------------------------------------------------------------------
# 3. CREATE A FUNCTION TO FETCH AND STORE ORDER BOOK
# -------------------------------------------------------------------
def fetch_and_store_orderbook(SYMBOL_LIST):
    """
    Fetch the order book for a given symbol from the exchange,
    then insert it into MongoDB.
    """
    for symbol in SYMBOL_LIST:
        try:
            # Step A: Fetch the order book (e.g., top 100 bids/asks)
            orderbook = exchange.fetch_order_book(symbol, limit=100)

            # Step B: Prepare document for MongoDB
            document = {
                "symbol": symbol,
                "bids": orderbook["bids"],
                "asks": orderbook["asks"],
                "timestamp": orderbook["timestamp"],  # exchange provided timestamp
                "datetime": datetime.utcnow()  # insertion time in UTC
            }

            # Step C: Insert into collection
            result = collection.insert_one(document)
            print(f"[{datetime.utcnow()}] Inserted document ID: {result.inserted_id}")

        except Exception as e:
            print(f"Error fetching or inserting order book data: {e}")


# -------------------------------------------------------------------
# 4. SCHEDULING TO FETCH EVERY 1 MINUTE
# -------------------------------------------------------------------
schedule.every(1).minutes.do(fetch_and_store_orderbook, SYMBOL_LIST)

if __name__ == "__main__":
    # Run indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep 1 second between checks
