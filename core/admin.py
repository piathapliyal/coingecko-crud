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
        ids = [c.coingecko_id for c in queryset if c.coingecko_id]
        data = fetch_prices_by_ids(ids, vs_currency="usd")
        updated = 0
        for coin in queryset:
            price = extract_decimal_price(data, coin.coingecko_id, "usd")
            if price is not None:
                coin.price = price
                coin.save(update_fields=["price"])
                updated += 1
        self.message_user(request, f"Updated {updated} coin(s).", level=messages.SUCCESS)

    # <-- this makes the price update as soon as you click SAVE
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.coingecko_id:
            data = fetch_prices_by_ids([obj.coingecko_id], vs_currency="usd")
            price = extract_decimal_price(data, obj.coingecko_id, "usd")
            if price is not None:
                obj.price = price
                obj.save(update_fields=["price"])
                self.message_user(request, f"Price updated to {obj.price}", level=messages.SUCCESS)
            else:
                self.message_user(request, "Could not fetch price from CoinGecko.", level=messages.WARNING)
