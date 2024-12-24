![License](https://img.shields.io/github/license/Moe-Dada/Multi-Asset-Crypto-Backtest)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CCXT](https://img.shields.io/badge/CCXT-1.95.72-yellow)

# L2 Market Data Capture

This repository provides a Python script to fetch Level-2 (L2) order book data from Binance (via [CCXT](https://github.com/ccxt/ccxt)) and store that data into a MongoDB collection. It includes:

1. **DataCapture.py**: Main script that connects to MongoDB, fetches order book data (bids and asks) for specified symbols, and inserts the data into MongoDB.  
2. **tests/**: Contains test modules (e.g., `test_DataCapture.py`) that use [mongomock](https://github.com/mongomock/mongomock) to mock MongoDB and `unittest.mock` to mock the exchange calls.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multiple Symbols**: Fetch order books for a list of symbols (e.g., BTC/USDT, ETC/USDT, etc.).  
- **MongoDB Storage**: Store each order book in a MongoDB collection, including:
  - Bids and asks  
  - Exchange-provided timestamp  
  - Local UTC insertion time  
- **Scheduling**: Fetch and store data at a regular interval (e.g., every 1 minute) using [schedule](https://github.com/dbader/schedule).
- **Tests**: Fully tested with `pytest` and `mongomock`.

---

## Requirements

- **Python 3.7+**  
- **MongoDB** (local or remote)  
- [CCXT](https://github.com/ccxt/ccxt)  
- [schedule](https://github.com/dbader/schedule)  
- [pymongo](https://pypi.org/project/pymongo/)  
- [mongomock](https://github.com/mongomock/mongomock) (for tests)  
- [pytest](https://docs.pytest.org/) (for tests)  

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<username>/<repo_name>.git
   cd <repo_name>
   ```

2. **Create and activate a virtual environment (optional, but recommended)**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

Or, if you prefer installing them manually:

```bash
pip install ccxt schedule pymongo mongomock pytest
```
---
## Usage
1. **MongoDB Connection**
By default, the code connects to `mongodb://127.0.0.1:27017/` with a database name of `market_data` and a collection name of `orderbooks`.

If you need to customize the URI, edit the variable `MONGO_URI` in `DataCapture.py`. For example, if you're using MongoDB Atlas, you can set:

```python
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```
2. **Select Symbols**
Update the `SYMBOL_LIST` in `DataCapture.py` to specify which symbols to fetch. For example:

```python
SYMBOL_LIST = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
```
3. **Running the Script**
To start capturing data, simply run:

```bash
python DataCapture.py
```
- The script will fetch data for the specified symbols every minute (by default) and insert it into the `market_data.orderbooks` collection.
- The scheduling interval can be changed in the line:

```python
schedule.every(1).minutes.do(fetch_and_store_orderbook, SYMBOL_LIST)
```
For example, you can change `.minutes` to `.seconds`, `.hours`, etc., as needed.
4. **Viewing Data**
Once data starts flowing into MongoDB, you can view it by connecting to your MongoDB instance:

```bash
# For a local MongoDB
mongosh
use market_data
db.orderbooks.find().pretty()
```
5. **Configuration**
- Exchange:
The code uses Binance via CCXT by default. If you want to use another exchange, update:

```python
exchange = ccxt.binance({
    "enableRateLimit": True
})
```
to:

```python
exchange = ccxt.<another_exchange>({
    "enableRateLimit": True
})
```
Make sure that exchange is supported by CCXT and you have any necessary API keys or credentials (if required).

- Limit:
The `fetch_order_book` function is set to fetch the top 100 levels. You can adjust the `limit` parameter:

```python
orderbook = exchange.fetch_order_book(symbol, limit=100)
```
---
## Testing
This repository uses `pytest` and `mongomock` to test database interactions without connecting to a real MongoDB instance.

1. **Install `pytest` and `mongomock` (if not already installed)**:

```bash
pip install pytest mongomock
```
2. **Run Tests:**

```bash
pytest
```

This will:

- Mock the exchange calls (using `unittest.mock.patch`)
- Mock the MongoDB collection (using `mongomock`)
- Verify that the function `fetch_and_store_orderbook` behaves correctly by checking if documents are inserted as expected.
3. **Test Output:**
If successful, you should see something like:

```diff
Copy code
================== test session starts ==================
...
collected 1 item

test_DataCapture.py .                                     [100%]

=================== 1 passed in 0.XXs ====================
```
---
## Contributing
1. **Fork the repository**
2. **Create a new branch (git checkout -b feature-branch)**
3. **Commit your changes (git commit -m 'Add some feature')**
4. **Push to the branch (git push origin feature-branch)**
5. **Open a Pull Request**
- We welcome any ideas, bug fixes, or improvements!
---
## License
MIT License
