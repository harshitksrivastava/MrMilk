from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Brand, Order, Profile, OrderDetail
from .permissions import UpdateOwnProfile
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, OrderSerializer, \
    OrderDetailSerializer, ProfileSerializer, LoginSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile, )

    # PATCH request is directed to this method for User Profile comes with detail=True
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "this is partial update for the User profile"}
        return Response(response, status=status.HTTP_200_OK)

    # PUT request is directed to this method for User Profile comes with detail=True
    def update(self, request, *args, **kwargs):
        response = {"message": "this is update for the User profile"}
        return Response(response, status=status.HTTP_200_OK)

    # DESTROY request is directed to this method for User Profile comes with detail=True
    def destroy(self, request, *args, **kwargs):
        response = {"message": "this is destroy for the User profile"}
        return Response(response, status=status.HTTP_200_OK)


# To Login a User with valid credentials and return Token along with successful message
class LoginAPIView(APIView):
    permission_classes = (UpdateOwnProfile, AllowAny)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(phone=serializer.data.get('phone'),
                                password=serializer.data.get('password'))
            if user is not None:
                return Response({"message": "Login Successful", "data": {
                    "token": Token.objects.get_or_create(user=user)[0].key}},
                                status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Phone or Password Incorrect", "data":
                        serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


# To register a user
class UserProfileCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    model = Profile
    serializer_class = ProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    List all the products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'list/(?P<category>[\w-]+)', url_name='category-list')
    def product_category(self, request, category=None):
        category_product = self.queryset.filter(category=category)
        serializer = self.serializer_class(category_product, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    """
    List all the categories
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get(self):
    #     brand_list = self.get_queryset()
    #     serializer = self.serializer_class(brand_list, many=True)
    #     return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, pk=None):
        order = get_object_or_404(self.queryset, pk)
        serializer = self.serializer_class(order, many=True)
        response = {'message': 'data is', 'data': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        order = Order.objects.filter(customer_id=pk)
        serializer = self.serializer_class(order, many=True)
        response = {'message': 'order list', 'data': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            # print("in the create of class of orderViewset")
            customer = Profile.objects.get(pk=request.data['customer_id'])
            # print("in the create of class of orderViewset2")
            serializer = self.get_serializer(data=request.data)
            # print("in the create of class of orderViewset3")
            if serializer.is_valid():
                serializer.save()
                # print("in the create of class of orderViewset4")
                response = {"message": "inserted data in order", "data": serializer.data}
                return serializer.data
        except:
            response = {"message": "not a registered user", "error": Exception}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    # def list(self, request, *args, **kwargs):
    #     response = {'message': 'you can not access full list'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(order_id=pk)
            order_detail = OrderDetail.objects.filter(order_id=pk)
            serializer = self.serializer_class(order_detail, many=True)
            # product_list = Product.objects.filter(serializer.data['product'])
            response = {'message': 'order_id wise order_detail', 'data': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'order_id does not exist in order_detail'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # print(request.data, len(request.data), type(request.data))
        serializer_order = OrderSerializer(data=request.data['order'])
        if serializer_order.is_valid():
            serializer_order.save()
            print(serializer_order.data)
            order_detail = request.data['order_detail']
            try:
                for data_item in order_detail:
                    d = dict(data_item)
                    d['order'] = serializer_order.data['order_id']
                    print(d['order'])
                    print(d['product'])
                    print(d['quantity'])
                    serializer_order_detail = self.get_serializer(data=d)
                    if serializer_order_detail.is_valid():
                        serializer_order_detail.save()
                    else:
                        print("not a valid serializer for order detail")
                        response = {'message': 'order already contains this product cannot change the it'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                data = OrderDetail.objects.filter(order_id=serializer_order.data['order_id'])
                serializer = self.serializer_class(data, many=True)
                response = {"message": "order detail inserted for", "order_data": serializer.data,
                            "order": serializer_order.data}
                return Response(response, status=status.HTTP_201_CREATED)
            except:
                response = {'message': 'order already contains this product cannot change the it'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("not a valid serializer for order")
            response = {'message': 'order already contains this product cannot change the it'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request, *args, **kwargs):
        response = {'message': 'you can not access full list'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(order_id=pk)
            order_detail = OrderDetail.objects.filter(order_id=pk)
            serializer = self.serializer_class(order_detail, many=True)
            # product_list = Product.objects.filter(serializer.data['product'])
            response = {'message': 'order_id wise order_detail', 'data': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'order_id does not exist in order_detail'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # print(request.data, len(request.data), type(request.data))
        serializer_order = OrderSerializer(data=request.data['order'])
        if serializer_order.is_valid():
            serializer_order.save()
            print(serializer_order.data)
            order_detail = request.data['order_detail']
            try:
                for data_item in order_detail:
                    d = dict(data_item)
                    d['order'] = serializer_order.data['order_id']
                    print(d['order'])
                    print(d['product'])
                    print(d['quantity'])
                    serializer_order_detail = self.get_serializer(data=d)
                    if serializer_order_detail.is_valid():
                        serializer_order_detail.save()
                    else:
                        print("not a valid serializer for order detail")
                        response = {'message': 'order already contains this product cannot change the it'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                data = OrderDetail.objects.filter(order_id=serializer_order.data['order_id'])
                serializer = self.serializer_class(data, many=True)
                response = {"message": "order detail inserted for", "order_data": serializer.data,
                            "order": serializer_order.data}
                return Response(response, status=status.HTTP_201_CREATED)
            except:
                response = {'message': 'order already contains this product cannot change the it'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("not a valid serializer for order")
            response = {'message': 'order already contains this product cannot change the it'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
