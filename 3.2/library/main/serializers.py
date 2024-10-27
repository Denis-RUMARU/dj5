from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import Book, Order

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['order_count'] = instance.order_set.count()
        return representation


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user_name = validated_data.get('user_name')
        active_orders_count = Order.objects.filter(user_name=user_name, is_active=True).count()

        if active_orders_count >= 10:
            raise ValidationError("Вы не можете создать более 10 активных заказов.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'is_active' in validated_data and validated_data['is_active']:
            user_name = validated_data.get('user_name', instance.user_name)
            active_orders_count = Order.objects.filter(user_name=user_name, is_active=True).count()

            if active_orders_count >= 10:
                raise ValidationError("Вы не можете иметь более 10 активных заказов.")

        return super().update(instance, validated_data)

    def delete(self, instance):
        return super().delete(instance)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        books = instance.books.all()
        serialized_books = BookSerializer(books, many=True).data
        representation['books'] = serialized_books
        return representation
