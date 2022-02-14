from rest_framework import serializers
from .models import Boxes
from datetime import datetime


class BoxAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Boxes
        fields = ('length', 'width', 'height', 'created_by')


class BoxUpdateSerializer(serializers.ModelSerializer):
    last_updated = serializers.HiddenField(
        default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    class Meta:
        model = Boxes
        fields = ('length', 'width', 'height', 'last_updated')


class BoxListUnrestrictedSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField()

    class Meta:
        model = Boxes
        fields = ('id', 'length', 'width', 'height', 'area',
                  'volume', 'last_updated', 'created_by')


class BoxListRestrictedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boxes
        fields = ('length', 'width', 'height', 'area', 'volume')
