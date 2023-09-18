from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.templatetags.static import static
from rest_framework import fields, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import dwollav2
import plaid
from plaid.api import plaid_api
import os

from .models import DwollaCustomer, DwollaFundingSource, DwollaTransferSource, PlaidToken
from .serializers import DwollaCustomerSerializer, DwollaFundingSourceSerializer, DwollaTransferSourceSerializer, PlaidTokenSerializer
from apps.web import serializers

app_key = os.environ.get("DWOLLA_APP_KEY")
app_secret = os.environ.get("DWOLLA_APP_SECRET")
dwolla_base_api = os.environ.get("DWOLLA_BASE_API")
dwolla_master_funding_source_id = os.environ.get("DWOLLA_MASTER_FUNDING_SOURCE_ID")
dwolla_client = dwollav2.Client(key = app_key, secret = app_secret, environment = 'sandbox') # optional - defaults to production
app_token = dwolla_client.Auth.client()

plaid_client_id = os.environ.get("PLAID_CLIENT_ID")
plaid_secret = os.environ.get("PLAID_SECRET")
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': plaid_client_id,
        'secret': plaid_secret,
    }
)
api_client = plaid.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'web/app_home.html', context={
            'active_tab': 'dashboard',
        })
    else:
        return render(request, 'web/landing_page.html')

@method_decorator(login_required, name='dispatch')
class ObjectLifecycleView(TemplateView):
    def get_context_data(self, **kwargs):
        return {}

class ReactView(ObjectLifecycleView):
    template_name = 'web/app_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'url_base': reverse('web:react_object_home'),
            'active_tab': 'dashboard',
        })
        return context
    
class PlaidApiViewSet(viewsets.ModelViewSet):
    queryset = PlaidToken.objects.all()
    serializer_class = PlaidTokenSerializer
    
    def get_queryset(self):
        return self.request.user.plaid_tokens.all()
    
    def retrieve(self, request, pk=None):
        user = self.request.user
        customer = DwollaCustomer.objects.get(user=user)
        serializer = DwollaCustomerSerializer(customer)
        client_user_id = serializer.data['customer_id']
        # Create a link_token for the given user
        request = {
            "products": ["auth"],
            "client_name": serializer.data['first_name'] + " " + serializer.data['last_name'],
            "country_codes": ['US'],
            "language": 'en',
            "webhook": 'https://webhook.example.com',
            "user": {
                'client_user_id': client_user_id
            }
        }
        response = plaid_client.link_token_create(request)
        return JsonResponse({
            'status': True,
            'data': '',
            'link_token': response['link_token']
        })
        
    def create(self, request, *args, **kwargs):
        data = request.data
        # Exchange the public token from Plaid Link for an access token.
        exchange_request = {"public_token":data['public_token']}
        exchange_token_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_token_response['access_token']
        
        # Create a processor token for a specific account id.
        create_request = {
            'access_token':access_token,
            "account_id":data['account_id'],
            "processor":'dwolla'
        }
        create_response = plaid_client.processor_token_create(create_request)
        processor_token = create_response['processor_token']
        customer_url = dwolla_base_api + "customers/" + data['link_token']
        request_body = {
            'plaidToken': processor_token,
            'name': data['account_id']
        }
        funding_source = app_token.post('%s/funding-sources' % customer_url, request_body)
        funding_source = app_token.get(funding_source.headers['location'])
        
        new_customer = DwollaFundingSource.objects.create(
            user=self.request.user,
            funding_id=funding_source.body['id'],
            status=funding_source.body['status'],
            type=funding_source.body['type'],
            bank_account_type=funding_source.body['bankAccountType'],
            name=funding_source.body['name'],
            bank_name=funding_source.body['bankName'],
            fingerprint=funding_source.body['fingerprint'],
            channels=",".join(funding_source.body['channels']),
        )
        new_customer.save()
        return JsonResponse({
            'status': True,
            'message': 'Successfully created!'
        })
        
        
    
class DwollaCustomerViewSet(viewsets.ModelViewSet):
    queryset = DwollaCustomer.objects.all()
    serializer_class = DwollaCustomerSerializer

    def get_queryset(self):
        return self.request.user.dwolla_customers.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            request_body = {
                'firstName': data['first_name'],
                'lastName': data['last_name'],
                'email': data['email'],
                'type': 'personal',
                'address1': data['address1'],
                'city': data['city'],
                'state': data['state'],
                'postalCode': data['postal_code'],
                'dateOfBirth': data['date_of_birth'],
                'ssn': data['ssn'],
            }
            new_customer = app_token.post('customers', request_body)
            new_customer = app_token.get(new_customer.headers['location'])
            new_customer = DwollaCustomer.objects.create(
                user=self.request.user,
                customer_id=new_customer.body['id'],
                status=new_customer.body['status'],
                first_name=new_customer.body['firstName'],
                last_name=new_customer.body['lastName'],
                email=new_customer.body['email'],
                type=new_customer.body['type'],
                address1=new_customer.body['address1'],
                city=new_customer.body['city'],
                state=new_customer.body['state'],
                postal_code=new_customer.body['postalCode'],
                date_of_birth=data['date_of_birth'],
                ssn=data['ssn']
            )
            new_customer.save()
            serrializer = DwollaCustomerSerializer(new_customer)
            return JsonResponse({
                'status': True,
                'data': serrializer.data,
                'message': 'Successfully created!'
            })        
        except:
            return JsonResponse({
                'status': False,
                'message': 'Something is wrong. Please try again later.'
            }) 
        
        

class DwollaFundingSourceViewSet(viewsets.ModelViewSet):
    queryset = DwollaFundingSource.objects.all()
    serializer_class = DwollaFundingSourceSerializer

    def get_queryset(self):
        return self.request.user.dwolla_funding_sources.all()
    
    def retrieve(self, request, pk=None):
        user = self.request.user      
        customer = DwollaCustomer.objects.get(user=user)
        serializer = DwollaCustomerSerializer(customer)
        # client_user_id = serializer.data['customer_id']
        # customer_url = dwolla_base_api + 'customers/' + client_user_id
        # funding_sources = app_token.get('%s/funding-sources' % customer_url)
        # funding_sources = funding_sources.body['_embedded']['funding-sources']
        # balance_id = ''
        # for funding in funding_sources:
        #     if (funding['name'] == 'Balance'):
        #         balance_id = funding['id']
        # funding_source_url = dwolla_base_api + 'funding-sources/' + balance_id
        # funding_source = app_token.get(funding_source_url)
        return JsonResponse({
            'status': True,
            'data': serializer.data['balance'],
        })

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DwollaTransferSourceViewSet(viewsets.ModelViewSet):
    queryset = DwollaTransferSource.objects.all()
    serializer_class = DwollaTransferSourceSerializer

    def get_queryset(self):
        return self.request.user.dwolla_transfer_sources.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user
        customer = DwollaCustomer.objects.get(user=user)
        if ((data['type'] == 'withdraw') and (float(data['amount']) > customer.balance)):
            return JsonResponse({
                'status': True,
                'data': '',
                'message': "You can withdraw less than balance."
            }) 
        request_body = {
            '_links': {
                'source': {
                    'href': dwolla_base_api + 'funding-sources/' + data['funding_id']
                },
                'destination': {
                    'href': dwolla_base_api + 'funding-sources/' + dwolla_master_funding_source_id
                }
            },
            'amount': {
                'currency': 'USD',
                'value': data['amount']
            },
        }
        
        if data['type'] == 'withdraw':
            request_body = {
                '_links': {
                    'source': {
                        'href': dwolla_base_api + 'funding-sources/' + dwolla_master_funding_source_id
                    },
                    'destination': {
                        'href': dwolla_base_api + 'funding-sources/' + data['funding_id']
                    }
                },
                'amount': {
                    'currency': 'USD',
                    'value': data['amount']
                },
            }

        transfer = app_token.post('transfers', request_body)
        transfer = app_token.get(transfer.headers['location'])
        dwolla_transfer = DwollaTransferSource.objects.create(
            user=user,
            transfer_id=transfer.body['id'],
            status=transfer.body['status'],
            type=data['type'],
            funding_id=data['funding_id'],
            amount=transfer.body['amount']['value'],
            currency=transfer.body['amount']['currency'],
            clearing=str(transfer.body['clearing'])
        )
        dwolla_transfer.save()
        
        message = 'Successfully deposited!'
        if data['type'] == 'withdraw':
            message = 'Successfully widthrawed!'
            customer.balance -= float(transfer.body['amount']['value'])
        else:
            customer.balance += float(transfer.body['amount']['value'])          
        customer.save()
        
        return JsonResponse({
            'status': True,
            'data': '',
            'message': message
        }) 
        