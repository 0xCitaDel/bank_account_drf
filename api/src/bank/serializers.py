from rest_framework import serializers
from .models import Customer, Account, Action

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('user_id', 'first_name', 'last_name',
                  'city', 'house', 'image')
        read_only_fields = ('user_id', )

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)


class AccountSerializer(serializers.ModelSerializer):

    actions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'user_id', 'balance', 'actions')
        read_only_fields = ('id', 'user_id', 'balance', 'actions')


class ActionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        if validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError(('Amonut must be positive'))

        return super().create(validated_data)

