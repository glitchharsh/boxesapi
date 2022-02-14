from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


BOX_AREA_LIMIT = 100
BOX_VOLUME_LIMIT = 1000
BOXES_IN_A_WEEK = 100
BOXES_IN_A_WEEK_BY_ONE_USER = 50

today = make_aware(datetime.now())
last_week = today - timedelta(days=today.isocalendar()[2])
end_of_last_week = last_week.replace(
    hour=23, minute=59, second=59, microsecond=999999)
end_of_last_week.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def area_validator(value):
    area_list = [int(ele[0])
                 for ele in list(Boxes.objects.all().values_list('area'))]
    area_list.append(value)
    avg = sum(area_list)/len(area_list)
    if avg > BOX_AREA_LIMIT:
        raise serializers.ValidationError(
            {"Area": ["Average area of all boxes exceeded the limit"]})
    else:
        return value


def volume_validator(value):
    last_week_volumes = Boxes.objects.filter(
        last_updated__gte=end_of_last_week).values_list('volume')
    volume_list = [int(ele[0]) for ele in list(last_week_volumes)]
    volume_list.append(value)
    avg = sum(volume_list)/len(volume_list)
    if avg > BOX_VOLUME_LIMIT:
        raise serializers.ValidationError(
            {"Volume": ["Average volume of all boxes in this week exceeded the limit"]})
    else:
        return value


def boxes_in_a_week_validator(value):
    last_week_boxes = Boxes.objects.filter(
        last_updated__gte=end_of_last_week).count()
    if last_week_boxes > (BOXES_IN_A_WEEK - 1):
        raise serializers.ValidationError(
            {"last_updated": ["Total number of boxes created in this week exceeded the limit"]})
    else:
        return value


def boxes_in_a_week_by_user_validator(value):
    last_week_boxes = Boxes.objects.filter(
        last_updated__gte=end_of_last_week, created_by=value).count()
    if last_week_boxes > (BOXES_IN_A_WEEK_BY_ONE_USER - 1):
        raise serializers.ValidationError(
            {"created-by": ["Total number of boxes created by user in this week exceeded the limit"]})
    else:
        return value


class Boxes(models.Model):
    length = models.FloatField(validators=[MinValueValidator(0.001)])
    width = models.FloatField(validators=[MinValueValidator(0.001)])
    height = models.FloatField(validators=[MinValueValidator(0.001)])
    area = models.FloatField(
        validators=[area_validator, boxes_in_a_week_validator])
    volume = models.FloatField(validators=[volume_validator])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, validators=[
                                   boxes_in_a_week_by_user_validator])
    last_updated = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.area = 2*((self.length*self.width)+(self.length *
                       self.height)+(self.width*self.height))
        self.volume = self.length*self.width*self.height
        self.full_clean()
        super(Boxes, self).save(*args, **kwargs)
