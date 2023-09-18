from django.urls import path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.home, name='home'),
    path('', views.ReactView.as_view(), name='react_object_home'),
    path('terms', TemplateView.as_view(template_name="web/terms.html"), name='terms'),
    path('404', TemplateView.as_view(template_name='404.html'), name='404'),
    path('500', TemplateView.as_view(template_name='500.html'), name='500'),
    # path('api/dwollav2/customers', views.DwollaCustomersAPIView.as_view(), name='customers'),
    # path('api/dwollav2/customers/<int:id>', views.DwollaCustomerAPIView.as_view(), name='customers'),
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
]

# drf config
router = routers.DefaultRouter()
router.register('api/dwollav2/customers', views.DwollaCustomerViewSet)
router.register('api/dwollav2/plaid', views.PlaidApiViewSet)
router.register('api/dwollav2/funding_sources', views.DwollaFundingSourceViewSet)
router.register('api/dwollav2/transfer_sources', views.DwollaTransferSourceViewSet)

urlpatterns += router.urls
