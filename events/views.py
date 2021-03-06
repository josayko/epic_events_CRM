from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import EventPermission, isManagement
from events.models import Event, EventStatus
from events.serializers import EventSerializer


class EventViewset(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, isManagement | EventPermission]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    # /events/?status=1
    filterset_fields = ["status"]
    # /events/?search=apple
    search_fields = [
        "^contract__client__company_name",
        "^contract__client__last_name",
        "^contract__client__email",
    ]

    def get_queryset(self):
        """
        Get all events
        """
        if self.request.user.role == "SALES":
            return Event.objects.filter(contract__sales_contact=self.request.user)
        elif self.request.user.role == "SUPPORT":
            return Event.objects.filter(support_contact=self.request.user)
        return Event.objects.all()

    def perform_create(self, serializer):
        """
        Cannot create an event:
        - with a prospect
        - an unknown contract
        - a non-signed contract
        - a contract that already have an event
        """
        if serializer.validated_data.get("contract").client.is_customer is False:
            raise PermissionDenied("Cannot create an event with a prospect")
        if serializer.validated_data.get("contract").id is None:
            raise PermissionDenied("Cannot create an event with an unknown contract")
        if serializer.validated_data.get("contract").is_signed is False:
            raise PermissionDenied("Cannot create an event with a non-signed contract")
        if Event.objects.filter(contract=serializer.validated_data.get("contract")).exists():
            raise PermissionDenied("An event is already set to this contract")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Cannot update a 'Done' event
        """
        event = self.get_object()
        done_status = EventStatus.objects.get(description="Done")
        if event.status == done_status:
            if serializer.validated_data.get("status") != done_status:
                raise PermissionDenied("Cannot update, event is already done")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
