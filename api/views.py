import warnings
from django.template import loader

import django_filters
from django.db.models import QuerySet, Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from .models import userInfo
from .serializers import userInfoSerializer, EmailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, filterset
from rest_framework.settings import api_settings
from django_filters import rest_framework as filters, utils, compat

# Create your views here.


"""class userInfoViewSet(viewsets.ModelViewSet):
    queryset = userInfo.objects.all().order_by('id')
    serializer_class = userInfoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['firstname', 'lastname']"""

"""class userInfoViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = userInfo.objects.all()
        serializer = userInfoSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = userInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = userInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = userInfoSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = userInfo.objects.get(pk=pk)
        serializer = userInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = userInfo.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

"""class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = userInfoSerializer
    queryset = userInfo.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)"""


"""class userInfoFilter(filters.Filter):
    email = filters.CharFilter(lookup_expr='icontains')
    firstname = filters.CharFilter(lookup_expr='icontains')
    lastname = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = userInfo
        fields = ('firstname', 'lastname', 'address', 'email', 'phone')"""


class userInfoFilter(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset


class userInfoList(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    #users = userInfo.objects.all()
    #filter_class = userInfoFilter
    serializer_class = userInfoSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    #filter_backends = (filters.DjangoFilterBackend,)

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ('firstname', 'lastname', 'address', 'email', 'phone')

    """def filter_queryset(self, users):
        for backend in list(self.filter_backends):
            users = backend().filter_queryset(self.request, users, self)
        return users"""

    """def get_queryset(self):
        users = userInfo.objects.all()
        firstname = self.request.query_params.get('firstname', None)
        email = self.request.query_params.get('email', None)
        if firstname is not None:
            users = users.filter(firstname=firstname)
        if email is not None:
            users = users.filter(email=email)
        return users"""

    def get(self, request, format=None):
        #users = userInfo.objects.all()
        get_page_number = request.query_params.get('page', None)
        if not get_page_number:
            get_page_number = 1

        """user = userInfo.objects.raw('SELECT * FROM api_userinfo LIMIT 2 OFFSET ' + str((int(get_page_number)-1)*2))
        for i in user:
            print(i)
        print(user)"""



        """ff = userInfoFilter()
        print(ff)
        filtered_queryset = ff.filter_queryset(request, users, self)
        print(filtered_queryset)"""

        offset = (int(get_page_number) - 1) * 10
        users = userInfo.objects.all()[offset:offset+10]



        #users_filtered = self.filter_queryset(users)[offset:offset + 2]
        #print(users_filtered)


        #print(request.query_params.get("page", None))


        # filtered_set = filters.userInfoFilter(self.users).qs


        #get_data = request.query_params

        #filtered_qs = self.get_queryset().filter(firstname=get_data['firstname'])
        #filtered_qs = self.filter_queryset(users)

        #filtered_qs = self.filter_queryset(users)
        """print(request)
        firstname = request.query_params.get('firstname', None)
        print(firstname)
        email = request.query_params.get('email', None)
        print(email)
        if firstname is not None:
            users = users.filter(firstname__icontains=firstname)
        if email is not None:
            users = users.filter(email__icontains=email)"""
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)
        """if filtered_queryset.exists():
            serializer = userInfoSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)"""

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def post(self, request, format=None):
        serializer = userInfoSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class userInfoDetail(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return userInfo.objects.get(id=id)
        except userInfo.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = userInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        serializer = userInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Filter(APIView):

    def get(self, request, data, format=None):
        users = userInfo.objects.filter(Q(firstname__icontains=data) | Q(lastname__icontains=data)).order_by('-id')
        serializer = userInfoSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""class FetchEmailsView(generics.ListCreateAPIView):
    queryset = userInfo.objects.all()
    serializer_class = EmailSerializer"""


class FetchEmailsView(APIView):
    def get(self, request):
        #get_data = request.query_params
        list = []
        users = userInfo.objects.all()
        print(users)

        #users = userInfo.objects.all().filter(fırstname=get_data['firstname'], email=get_data['email'])
        serializer = EmailSerializer(users, many=True)
        print(serializer)
        print(serializer)
        return Response(serializer.data)



"""class FetchEmailsView(APIView):

    def get(self, request):
        #users = [str(elem) for elem in list(userInfo.objects.all().values_list('firstname'))]
        users = userInfo.objects.all().values_list('firstname', flat=True)
        print(users)
        serializer = userInfoSerializer(users, many=True)
        print(serializer)
        return Response(serializer.data)"""




"""class ListItem(APIView):
    def get(self, request):
        get_data = request.query_params
        return userInfo.objects.filter(firstname=get_data['firstname']).order_by('id')"""


"""@api_view(['GET', 'POST'])
def list_users(request):
    if request.method == 'GET':
        users = userInfo.objects.all()
        serializer = userInfoSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = userInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

"""@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = userInfo.objects.get(pk=pk)
    except userInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = userInfoSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = userInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""
