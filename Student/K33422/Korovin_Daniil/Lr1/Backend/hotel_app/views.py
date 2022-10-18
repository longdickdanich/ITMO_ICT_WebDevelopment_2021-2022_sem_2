from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django_filters import filters, RangeFilter, DateFromToRangeFilter, ModelMultipleChoiceFilter, NumberFilter, \
    ChoiceFilter, MultipleChoiceFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import mixins
from rest_framework.filters import SearchFilter, BaseFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from hotel_app.models import Admin, Room, Client, Inhabitation, Cleaner, Cleaning, CleanerAvatar
from hotel_app.serializers import AdminSerializer, RoomSerializer, ClientSerializer, InhabitationSerializer, \
    CleanerSerializer, CleaningSerializer, CleanerAvatarSerializer, FileUploadsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.num_pages,
            'page': self.page.number,
            'results': data
        })


class DateFilter(FilterSet):
    in_date = DateFromToRangeFilter()

    class Meta:
        model = Inhabitation
        fields = ['in_date']


class CostOfLivingFilter(FilterSet):
    cost_of_living = RangeFilter()
    room_type = MultipleChoiceFilter(
        choices=Room.ROOM_TYPES
    )

    class Meta:
        model = Room
        fields = ['cost_of_living', 'room_type']


class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CostOfLivingFilter

    pagination_class = StandardResultsSetPagination
    # permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name', 'cost_of_living']
    filterset_fields = ['room_type']


class RoomFloorFilterView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(floor=self.kwargs['floor'])
        return queryset


class RoomNumbersFilterView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = self.queryset.filter(number__gte=self.kwargs['num_g'], number__lte=self.kwargs['num_l'])
        return queryset


class RoomFloorRoomTypeFilterView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.all()
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(floor=self.kwargs['floor'], room_type=self.kwargs['room_type'])
        return queryset


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]
    search_fields = ['full_name']


class InhabitationViewSet(ModelViewSet):
    queryset = Inhabitation.objects.all()
    serializer_class = InhabitationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DateFilter
    ordering_fields = ['in_date']
    ordering = ['in_date']
    pagination_class = StandardResultsSetPagination


class CleanerViewSet(ModelViewSet):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerSerializer
    # permission_classes = [IsAuthenticated]


class CleaningViewSet(ModelViewSet):
    queryset = Cleaning.objects.all()
    serializer_class = CleaningSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    filter_fields = ['cleaner__full_name']
    search_fields = ['cleaning_day', 'cleaning_floor']
    ordering_fields = ['cleaning_day']
    ordering = ['cleaning_day']


class UploadAvatarClient(ViewSet):
    queryset = CleanerAvatar.objects.all()
    serializer_class = CleanerAvatarSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        file_uploaded = request.FILES.get('file_uploaded')
        cleaner = request.POST.get('cleaner')
        content_type = file_uploaded.content_type
        file_name = file_uploaded.name
        file_size = file_uploaded.size
        serializer = self.serializer_class(data={"file": file_uploaded, "cleaner": cleaner, "file_size": file_size})
        serializer.is_valid()
        serializer.save(file_name=file_name)
        response = f"POST API and you have uploaded a {content_type} file {file_name}"
        return Response(response)


class UploadFiles(ViewSet):
    queryset = CleanerAvatar.objects.all()
    serializer_class = FileUploadsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        files = request.FILES.getlist('file')
        file_serializers = []
        for file in files:
            print(file)

            serializer = self.serializer_class(data={"file": file})
            try:
                serializer.is_valid(raise_exception=True)
                file_serializers.append(serializer)
            except ValidationError as err:
                return HttpResponseBadRequest(err)

        for serializer in file_serializers:
            serializer.save()
        response = f"POST API and you have uploaded files"
        return Response(response)
