from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import BitcoinSerializer
from .models import Bitcoin
from rest_framework import viewsets
import requests

from datetime import timezone
import datetime
from django.utils.timezone import make_aware
  
import pytz


# Create your views here.

@api_view(['GET'])
def data(request):
    bitcoin = Bitcoin.objects.all()
    bitcoin = BitcoinSerializer(bitcoin, many=True)
    return JsonResponse(bitcoin.data, safe=False)

class BitcoinViewSet(viewsets.ModelViewSet):
    def get_queryset_data(self):
        data = Bitcoin.objects.all()
        return data

    def save_bitcoin_data(self):
        res = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin')
        response = res.json()
        price = response['market_data']['current_price']['usd']

        dt = datetime.datetime.now()
        dt_utc = dt.astimezone(pytz.UTC)
        bitcoin_object = Bitcoin.objects.create(price=price, timestamp=dt_utc)
        bitcoin_object.save()
