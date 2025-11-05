from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json   

from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')  
    serializer_class = ItemSerializer
   


@api_view(['GET'])
def fetch_btc(request):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    try:
        resp = requests.get(url, timeout=10)  # bumped timeout just in case
        data = resp.json()
        btc_usd = data.get('bitcoin', {}).get('usd', None)
    except Exception as e:
        print("BTC fetch failed -->", e)  
        return Response({"error": "fetch failed"}, status=500)

    if btc_usd is None:
        return Response({"error": "price not found"}, status=404)

    return Response({"btc_price": btc_usd})  


from django.db.models import Count
from django.shortcuts import render
from datetime import timedelta, date


def report(request):
    today = date.today()
    lastweek = today - timedelta(days=6)   

    qs = (
        Item.objects.filter(created_at__date__gte=lastweek)
        .extra({'day': "date(created_at)"})
        .values('day')
        .annotate(total=Count('id'))   
    )

  
    labels = []
    for i in range(7):
        d = str(lastweek + timedelta(days=i))
        labels.append(d)

   
    counts = {}
    for x in qs:
        counts[str(x['day'])] = x['total']

    data = []
    for label in labels:
        if label in counts:
            data.append(counts[label])
        else:
            data.append(0)

    return render(request, "report.html", {
        "labels": labels,
        "data": data,
       
    })
