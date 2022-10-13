from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import BitcoinSerializer
from .models import Bitcoin
from rest_framework import viewsets
import requests
import datetime
from django.core.mail import send_mail 
from django.core import mail
import pytz


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