from decimal import Decimal
import requests

API_BASE = "https://api.coingecko.com/api/v3"

def fetch_prices_by_ids(ids, vs_currency="usd"):
    if not ids:
        return {}
    r = requests.get(
        f"{API_BASE}/simple/price",
        params={"ids": ",".join(ids), "vs_currencies": vs_currency},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()

def extract_decimal_price(data, coin_id, vs_currency="usd"):
    try:
        return Decimal(str(data[coin_id][vs_currency]))
    except Exception:
        return None
