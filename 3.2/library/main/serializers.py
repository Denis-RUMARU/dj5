from rest_framework import serializers

from main.models import Book, Order


class BookSerializer(serializers.ModelSerializer):
    # реализуйте сериализацию объектов модели Book
    class Meta:
        model = Book
        fields = '__all__'

    #доп задание
    def to_representation(self, instance):
         representation = super().to_representation(instance)
         representation['order_count'] = instance.order_set.count()
         return representation


class OrderSerializer(serializers.ModelSerializer):
    # добавьте поля модели Order
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)

    def delete(self, instance):
        return super().delete(instance)

    #доп задание
    def to_representation(self, instance):
         representation = super().to_representation(instance)
         books = instance.books.all()
         serialized_books = BookSerializer(books, many=True).data
         representation['books'] = serialized_books
         return representation