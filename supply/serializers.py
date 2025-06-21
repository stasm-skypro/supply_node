# supply/serializers.py
from rest_framework import serializers

from supply.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = ["debt_to_supplier"]

    def update(self, instance, validated_data):
        # запрет на обновление поля debt_to_supplier
        if "debt_to_supplier" in validated_data:
            validated_data.pop("debt_to_supplier")
        return super().update(instance, validated_data)
