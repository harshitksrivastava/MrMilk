from rest_framework import serializers, fields
from MrMilk import models
from MrMilk.models import Order, OrderDetail


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('id', 'phone', 'name', 'password', 'address', 'is_staff', 'is_active', 'is_superuser')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'},
                'required': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = models.Brand
        fields = ('brand_name', 'products')


class OrderSerializer(serializers.ModelSerializer):
    # orders = OrderDetailSerializer(many=True)
    class Meta:
        model = models.Order
        fields = '__all__'

    # 'order_id', 'customer_id', 'order_status', 'delivery_date', 'order_address', 'total', 'transaction_id', 'cod')

    def create(self, validated_data):
        # correct the glitch for inserting same product differently for same order_id
        print("in the serializer creation class of orders")
        return Order.objects.create(**validated_data)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = ('order', 'quantity', 'product')

    def create(self, validated_data):
        print("in the serializer creation class of ordersDetail")
        result = OrderDetail.objects.create(**validated_data)
        return result
