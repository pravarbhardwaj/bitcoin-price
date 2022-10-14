from .serializers import BitcoinSerializer
from .models import Bitcoin
from rest_framework import viewsets
import requests
import datetime
from django.core import mail
import pytz
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination


class apiData(APIView):    
    def get(self, request):
        date = request.GET.get('date', '')
        bitcoin = Bitcoin.objects.all()
        if date:
            dt = datetime.datetime.strptime(date, f"%d-%m-%Y")
            start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
            bitcoin = bitcoin.filter(timestamp__range=(start, end))
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(bitcoin, request)
        bitcoinSerializedData = BitcoinSerializer(result_page, many=True)
        return_data = paginator.get_paginated_response(bitcoinSerializedData.data)
        return return_data

        
class BitcoinViewSet(viewsets.ModelViewSet):
    
    def get_queryset_data(self):
        data = Bitcoin.objects.all()
        return data

    def save_bitcoin_data(self):
        try:
            prevPrice = Bitcoin.objects.all().last()
            prevPrice = prevPrice.price if prevPrice else None
            res = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin')
            response = res.json()
            price = response['market_data']['current_price']['usd']
            dt = datetime.datetime.now()
            dt_utc = dt.astimezone(pytz.UTC)
            bitcoin_object = Bitcoin.objects.create(price=price, timestamp=dt_utc)
            bitcoin_object.save()
            if prevPrice and prevPrice != price:
                self.send_email(prevPrice, price)
        except Exception as e:
            print(e)

    def send_email(self, prevPrice, currPrice):
        try:
            email = mail.EmailMessage(
                'Bitcoin Price has changed',
                f'Bitcoin Price has changed from {prevPrice} USD to {currPrice} USD',
                'from@localdjangoapp',
                ['sandbox@mailtrap'],
            )
            email.send()
            print('BITCOIN PRICE CHANGED, EMAIL SENT')
        except Exception as e:
            print(e)