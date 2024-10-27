from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError

from main.models import Book, Order
from main.serializers import BookSerializer, OrderSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


@api_view(['GET'])
def books_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


class CreateBookView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Книга успешно создана', status=status.HTTP_201_CREATED)

class BookDetailsView(RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(UpdateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(DestroyAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_name = request.data.get('user_name')
        active_orders_count = Order.objects.filter(user_name=user_name, is_active=True).count()

        if active_orders_count >= 10:
            raise ValidationError("Вы не можете создать более 10 активных заказов.")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Проверка на открытое объявление
        if data.get('is_active', instance.is_active):
            user_name = data.get('user_name', instance.user_name)
            active_orders_count = Order.objects.filter(user_name=user_name, is_active=True).count()

            if active_orders_count >= 10:
                raise ValidationError("Вы не можете иметь более 10 активных заказов.")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'detail': 'Заказ успешно удален'}, status=status.HTTP_204_NO_CONTENT)
