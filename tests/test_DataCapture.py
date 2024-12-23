import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import mongomock

# Import your function from DataCapture.py
# (Adjust the import to match your actual file and function names.)
from DataCapture import fetch_and_store_orderbook


@pytest.fixture
def mock_db():
    """
    Create a mongomock MongoClient and return a reference to a test collection.
    """
    # Create an in-memory MongoClient using mongomock
    client = mongomock.MongoClient()

    # Use a test database (not "market_data" to avoid collisions)
    db = client["test_market_data"]
    collection = db["test_orderbooks"]

    # Return both db and collection for convenience
    return db, collection


@patch("DataCapture.exchange")  # Patching the entire exchange object
def test_fetch_and_store_orderbook(mock_exchange, mock_db):
    """
    Test that fetch_and_store_orderbook successfully fetches data
    and inserts it into MongoDB.
    """
    db, collection = mock_db

    # Mock the return value of exchange.fetch_order_book
    mock_exchange.fetch_order_book.return_value = {
        "bids": [[40000, 1.2], [39999.5, 0.8]],
        "asks": [[40001, 2.5], [40002, 0.3]],
        "timestamp": 1680000000000
    }

    # We'll override the global `collection` used in fetch_and_store_orderbook.
    # One way is to patch 'DataCapture.collection' directly.
    # Another is to pass the mock collection as an argument (shown below).

    # We'll do the simplest approach: patch 'DataCapture.collection'.
    with patch("DataCapture.collection", new=collection):
        # Now call the function to test with a single symbol
        test_symbols = ["BTC/USDT"]
        fetch_and_store_orderbook(test_symbols)

        # Verify that a document was inserted
        inserted_doc = collection.find_one({"symbol": "BTC/USDT"})
        assert inserted_doc is not None, "Expected document not inserted."

        # Check fields in the inserted document
        assert inserted_doc["symbol"] == "BTC/USDT"
        assert inserted_doc["bids"] == [[40000, 1.2], [39999.5, 0.8]]
        assert inserted_doc["asks"] == [[40001, 2.5], [40002, 0.3]]
        assert inserted_doc["timestamp"] == 1680000000000

        # 'datetime' should be inserted, but we only check existence
        assert "datetime" in inserted_doc
        assert isinstance(inserted_doc["datetime"], datetime)

    print("Test passed: Document was fetched and stored correctly.")
