from rest_framework import serializers
from bitcoin.models import Bitcoin

class BitcoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = ['timestamp', 'price']