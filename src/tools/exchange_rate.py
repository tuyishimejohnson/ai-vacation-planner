from dotenv import load_dotenv
import os
import requests

load_dotenv()
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    amount: float | None = None,
) -> dict:
    """Get the latest exchange rate and optionally convert an amount."""

    base = from_currency.upper()
    target = to_currency.upper()

    url = (
        f"https://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_RATE_API_KEY}"
    )

    data = requests.get(url).json()

    if not data.get("success"):
        return {"error": data.get("error", {}).get("info", "Failed to get rates")}

    rates = data["rates"]
    api_base = data["base"]

    from_rate = 1 if base == api_base else rates[base]
    target_rate = 1 if target == api_base else rates[target]

    rate = target_rate / from_rate

    result = {
        "from": base,
        "to": target,
        "rate": rate,
    }

    if amount is not None:
        result["amount"] = amount
        result["converted"] = amount * rate

    return result
