from decimal import Decimal
import time
import requests

API_BASE = "https://api.coingecko.com/api/v3"


def fetch_prices_by_ids(ids, vs_currency="usd"):
    
    if not ids:
        return {}, False

    url = f"{API_BASE}/simple/price"
    params = {"ids": ",".join(ids), "vs_currencies": vs_currency}

    # Retry a few times if rate-limited
    for delay in (0, 1, 3, 5):
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 429:
            time.sleep(delay)
            continue
        try:
            r.raise_for_status()
            return r.json(), False
        except Exception:
            return {}, True

    return {}, True


def extract_decimal_price(payload, coin_id, vs_currency="usd"):
    try:
        value = payload[coin_id][vs_currency]
        return Decimal(str(value))
    except Exception:
        return None