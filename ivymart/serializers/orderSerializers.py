from rest_framework import serializers
from ivymart.models import Order, OrderItem, Payment
from ivymart.serializers.productSerializers import ShippingAddressSerializer
from ivymart.serializers.userSerializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    User = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_User(self, obj):
        items = obj.user
        serializer = UserSerializer(items, many=False)
        return serializer.data


class PaymentSerializer(serializers.ModelSerializer):
    User = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    def get_User(self, obj):
        items = obj.user
        serializer = UserSerializer(items, many=False)
        return serializer.data
