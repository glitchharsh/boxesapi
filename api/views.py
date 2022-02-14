from rest_framework import generics, serializers
from .serializers import BoxAddSerializer, BoxListRestrictedSerializer, BoxListUnrestrictedSerializer, BoxUpdateSerializer
from .models import Boxes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwner
from datetime import datetime


class BoxListAll(generics.ListAPIView):
    queryset = Boxes.objects.all()

    def get_serializer_class(self):
        self.filterset_fields = {
            'length': ['gt', 'lt'],
            'width': ['gt', 'lt'],
            'height': ['gt', 'lt'],
            'area': ['gt', 'lt'],
            'volume': ['gt', 'lt'],
        }

        if self.request.user.is_staff:
            self.filterset_fields['last_updated'] = ['gt', 'lt']
            self.filterset_fields['created_by'] = ['exact']
            return BoxListUnrestrictedSerializer
        return BoxListRestrictedSerializer


class BoxAdd(generics.CreateAPIView):

    queryset = Boxes.objects.all()
    serializer_class = BoxAddSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer,):
        serializer.save(created_by=self.request.user)


class BoxUpdate(generics.UpdateAPIView):
    queryset = Boxes.objects.all()
    serializer_class = BoxUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        now = datetime.now()
        serializer.save(last_updated=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))


class BoxDelete(generics.DestroyAPIView):
    queryset = Boxes.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwner]


class MyBoxes(generics.ListAPIView):
    queryset = Boxes.objects.all()

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BoxListUnrestrictedSerializer

    filterset_fields = {
        'length': ['gt', 'lt'],
        'width': ['gt', 'lt'],
        'height': ['gt', 'lt'],
        'area': ['gt', 'lt'],
        'volume': ['gt', 'lt'],
    }

    def get_queryset(self):
        return Boxes.objects.all().filter(created_by=self.request.user)
