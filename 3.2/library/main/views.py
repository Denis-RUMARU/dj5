from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Book, Order
from main.serializers import BookSerializer, OrderSerializer


@api_view(['GET'])
def books_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data)


class CreateBookView(APIView):
    def post(self, request):
        # получите данные из запроса
        serializer = BookSerializer(data=request.data) #передайте данные из запроса в сериализатор
        if serializer.is_valid(raise_exception=True): #если данные валидны
            return Response('Книга успешно создана') # возвращаем ответ об этом


class BookDetailsView(RetrieveAPIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            ser = BookSerializer(book)
            return Response(ser.data)
        except Book.DoesNotExist:
            return Response(status=404)


class BookUpdateView(UpdateAPIView):
        serializer_class = BookSerializer

        def patch(self, request, id):
            try:
                book = Book.objects.get(id=id)
                serializer = self.get_serializer(book, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response('Книга успешно обновлена')
            except Book.DoesNotExist:
                return Response(status=404)


class BookDeleteView(DestroyAPIView):
    # реализуйте логику удаления объявления
    def delete(self, request, id):
        try:
            product = Book.objects.get(id=id)
            product.delete()
            return Response('Книга успешно удалена')
        except Book.DoesNotExist:
            return Response(status=404)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer