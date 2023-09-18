from rest_framework import serializers

from .models import DwollaCustomer, DwollaFundingSource, DwollaTransferSource, PlaidToken

class PlaidTokenSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PlaidToken
        fields = (
            'id',
            'user',
            'link_token',
            'public_token',
            'account_id',
            'created_at',
            'updated_at'
        )
    

class DwollaCustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = DwollaCustomer
        fields = (
            'id',
            'user',
            'balance',
            'is_active',
            'customer_id',
            'first_name',
            'last_name',
            'email',
            'status',
            'ip_address',
            'type',
            'address1',
            'address2',
            'city',
            'state',
            'postal_code',
            'date_of_birth',
            'ssn',
            'phone',
            'correlation_id',
            'business_name',
            'doing_business_as',
            'business_type',
            'business_classification',
            'ein',
            'website',
            'controller',
            'created_at',
            'updated_at'
        )

class DwollaFundingSourceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = DwollaFundingSource
        fields = (
            'id',
            'user',
            'is_active',
            'funding_id',
            'status',
            'type',
            'bank_account_type',
            'name',
            'bank_name',
            'fingerprint',
            'channels',
            'created_at',
            'updated_at'
        )
        
class DwollaTransferSourceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = DwollaTransferSource
        fields = (
            'id',
            'user',
            'status',
            'funding_id',
            'transfer_id',
            'amount',
            'amount',
            'currency',
            'type',
            'clearing',
            'created_at',
            'updated_at'
        )