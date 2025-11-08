from django.contrib import admin, messages
from .models import Coin
from .services.coingecko import fetch_prices_by_ids, extract_decimal_price


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "symbol", "coingecko_id", "price", "created_at")
    search_fields = ("name", "symbol", "coingecko_id")
    actions = ["fetch_latest_price"]

    @admin.action(description="Fetch latest price from CoinGecko")
    def fetch_latest_price(self, request, queryset):
        ids = sorted({c.coingecko_id for c in queryset if c.coingecko_id})
        data, limited = fetch_prices_by_ids(ids, vs_currency="usd")

        updated = 0
        for coin in queryset:
            p = extract_decimal_price(data, coin.coingecko_id, "usd")
            if p is not None:
                coin.price = p
                coin.save(update_fields=["price"])
                updated += 1

        if limited:
            self.message_user(request, "CoinGecko rate limit reached. Try again in 30 seconds.", level=messages.WARNING)
        else:
            self.message_user(request, f"Updated {updated} coin(s).", level=messages.SUCCESS)