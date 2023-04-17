from .serializers import CustomerSerializer, AccountSerializer, ActionSerializer
from .models import Customer, Account, Action

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, mixins, generics

class CurrentDataUserMixin:

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user)
        

class CustomerView(generics.RetrieveUpdateAPIView):

    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class AccountViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ActionViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Action.objects.all()

    def get_queryset(self):
        return self.queryset.filter(account__user=self.request.user)
