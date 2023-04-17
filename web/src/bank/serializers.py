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

    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'user_id', 'balance', 'actions')
        read_only_fields = ('id', 'user_id', 'balance', 'actions')


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        validated_data['account'].balance += validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)

