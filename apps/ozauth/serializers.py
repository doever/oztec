#!/usr/bin/python3
# -*- coding:utf-8 -*-
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid','username','telephone','email','data_joined']