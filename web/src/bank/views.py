from .serializers import CustomerSerializer
from .models import Customer

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        """Create a new customer"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)