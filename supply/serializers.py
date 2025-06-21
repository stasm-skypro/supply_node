# supply/serializers.py
from rest_framework import serializers

from supply.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = ["debt_to_supplier"]

    def update(self, instance, validated_data):
        validated_data.pop("debt_to_supplier", None)
        return super().update(instance, validated_data)
